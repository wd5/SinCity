# -*- coding: utf-8 -*-
import simplejson

from django.contrib import auth
from django.contrib.auth.decorators import  permission_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import flatpage

from forms import *
from models import *

def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict or {})
    return _render_to_response(template_name, context_instance=context)


def index(request):
    last_news = News.objects.all()[:5]
    return render_to_response(request, 'index.html', {'news': last_news})


def roles(request):
    roles = list(Role.objects.all().order_by('order'))
    return render_to_response(request, 'roles.html', {'roles':roles,})


def get_current_user(func):
    u"""Добавляет в параметры вьюхи игрока, анкету которого надо обработать"""
    def wrapper(request):
        def _get_user(request):
            change_user = None
            for source in (request.POST, request.GET):
                if source and source.get('change_user'):
                    change_user = source.get('change_user')

            if request.user and request.user.is_authenticated() and \
                request.user.is_superuser and change_user:
                    return User.objects.get(pk=change_user)

            return request.user

        return func(request, _get_user(request))

    return wrapper


@get_current_user
def request_form(request, current_user):
    context = {'current_user': current_user.id,
               'user_present': request.user.is_authenticated(),
               'admin': request.user.is_superuser,
    }

    if request.POST:
        profile = None
        if request.user and request.user.is_authenticated():
            profile = current_user.get_profile()

        else:
            context['reg_form'] = RegistrationForm(request.POST)

            if context['reg_form'].is_valid():
                # Вдруг он уже зареган
                login_form = LoginForm(request.POST)
                if login_form.is_valid():
                    request.user = login_form.user
                    profile = request.user.get_profile()
                    auth.login(request, request.user)
                    del context['reg_form']
                    current_user = request.user

                else:
                    try:
                        login_form.get_user(request.POST.get('login'))
                        context['message'] = u"Вы ввели неправильный пароль к своей учетной записи."
                    except User.DoesNotExist:
                        # Заводим нового пользователя
                        request.user = context['reg_form'].save()
                        profile = Profile.objects.create(user=request.user)
                        auth.login(request, request.user)
                        del context['reg_form']
                        current_user = request.user

        if profile:
            context['profile_form'] = ProfileForm(request.POST, request.FILES, instance=profile)
            if context['profile_form'].is_valid():
                context['profile_form'].save()

                if profile.role and request.POST.get('roles-TOTAL_FORMS'):
                    context['connections_formset'] = ConnectionFormSet(request.POST, instance=profile.role)
                    if context['connections_formset'].is_valid():
                        context['connections_formset'].save()

                    context['layers_formset'] = LayerFormSet(request.POST, instance=profile.role)
                    if context['layers_formset'].is_valid():
                        context['layers_formset'].save()

                return HttpResponseRedirect(reverse('form') + '?save=ok&change_user=%s' % current_user.id)

            else:
                if settings.DEBUG:
                    print context['profile_form'].str_errors()
        else:
            context['profile_form'] = ProfileForm(request.POST)

    else:
        if request.user and request.user.is_authenticated():
            context['profile_form'] = ProfileForm(instance=current_user.get_profile())
            role = current_user.get_profile().role
            context['connections_formset'] = ConnectionFormSet(instance=role, queryset=RoleConnection.objects.filter(role=role, is_locked=False))
            context['layers_formset'] = LayerFormSet(instance=role, queryset=LayerConnection.objects.filter(role=role, is_locked=False))
        else:
            context['profile_form'] = ProfileForm()
            context['reg_form'] = RegistrationForm()

    return render_to_response(request, 'form.html', context)


@get_current_user
def lock(request, current_user):
    if not request.user.is_superuser:
        raise Http404

    profile = current_user.get_profile()

    if request.GET.get('action') == 'lock':
        profile.lock(request.GET.get('field'))
        return HttpResponse(simplejson.dumps({'success':True}))

    elif request.GET.get('action') == 'unlock':
        profile.unlock(request.GET.get('field'))
        return HttpResponse(simplejson.dumps({'success':True}))

    raise Http404


@get_current_user
def lock_rel(request, current_user):
    if not request.user.is_superuser:
        raise Http404

    profile = current_user.get_profile()
    connection = RoleConnection.objects.get(pk=request.GET.get('rel'), role=profile.role)

    if request.GET.get('action') == 'lock':
        connection.is_locked = True
        connection.save()
        return HttpResponse(simplejson.dumps({'success':True}))

    elif request.GET.get('action') == 'unlock':
        connection.is_locked = False
        connection.save()

    raise Http404


def messages_compose(request):
    from messages.views import compose
    recipient = None
    if request.method == 'GET' and request.GET.get('recipient'):
        recipient = request.GET.get('recipient')
    return compose(request, recipient=recipient)


def bus(request):
    if request.user.is_authenticated() and request.GET:
        profile = request.user.get_profile()
        if request.GET.get('bus') == 'on':
            profile.bus = True
        elif request.GET.get('bus') == 'off':
            profile.bus = False
        profile.save(check_diff=False)
        return HttpResponseRedirect(reverse('bus'))

    context = {'passangers': Profile.objects.filter(bus=True),
               'page': FlatPage.objects.get(url='/bus'),
               }
    if request.user.is_authenticated():
        context['profile'] = request.user.get_profile()

    return render_to_response(request, 'bus.html', context)

############################################################################
# Reports

@permission_required('add_user')
def reports(request):
    return render_to_response(request, 'reports/index.html',
                              {'emails':", ".join(user.email for user in User.objects.all()),
                               'profiles': Profile.objects.all().order_by('role__ticket_level'),
                               'locked_roles_amount': Role.objects.filter(profile__isnull=False).count(),
                              })

@permission_required('add_user')
def report_actions(request):
    return render_to_response(request, 'reports/actions.html',
                          {'profiles': Profile.objects.filter(Q(wsl_actions__gt=0)|Q(gl_actions__gt=0))}
                          )

@permission_required('add_user')
def report_money(request):
    return render_to_response(request, 'reports/money.html',
                          {'profiles': Profile.objects.all()}
                          )


@permission_required('add_user')
def report_contacts(request):
    return render_to_response(request, 'reports/contacts.html',
                          {'profiles': Profile.objects.all().filter(role__isnull=False, locked_fields__contains='role').order_by('role__ticket_level', 'role__order')}
                          )


@permission_required('add_user')
def report_paid(request):
    return render_to_response(request, 'reports/paid.html',
                          {'profiles': Profile.objects.all().order_by('-paid', 'name')}
                          )

@permission_required('add_user')
def report_layers(request):
    return render_to_response(request, 'reports/layers.html',
                          {'layer_connections': LayerConnection.objects.all().order_by('layer', 'role')}
                          )


@permission_required('add_user')
def report_players_without_roles(request):
    return render_to_response(request, 'reports/players_without_roles.html',
                          {'profiles': Profile.objects.exclude(locked_fields__contains='role').order_by('name')}
                          )