# -*- coding: utf-8 -*-
from django.utils import simplejson

from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.db.models import F

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
    roles = list(Role.objects.all().order_by('rolesection__order', 'order'))
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


def __messages_compose(request):
    from messages.views import compose
    recipient = None
    if request.method == 'GET' and request.GET.get('recipient'):
        role = Role.objects.get(pk=request.GET.get('recipient'))
        recipient = str(role.id)
    return compose(request, recipient=recipient, form_class=ComposeForm)

@login_required
def messages_compose(request, template_name='messages/compose.html', success_url=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        sender = request.user
        form = ComposeForm(request.POST)
        if form.is_valid():
            form.save(sender=request.user)
            request.user.message_set.create(
                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if request.GET.has_key('next'):
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = ComposeForm(initial=request.GET)

    return render_to_response(request, template_name, {
        'form': form,
        })


@login_required
def reply(request, message_id, form_class=ComposeForm,
          template_name='messages/compose.html', success_url=None, recipient_filter=None):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote.
    """
    from messages.utils import format_quote
    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            request.user.message_set.create(
                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class({
            'body': _(u"%(sender)s wrote:\n%(body)s") % {
                'sender': parent.sender.get_profile().role.name,
                'body': format_quote(parent.body)
            },
            'subject': _(u"Re: %(subject)s") % {'subject': parent.subject},
            'recipient': parent.sender.get_profile().role_id
        })
    return render_to_response(request, template_name, {
        'form': form,
        })


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
               }
    if request.user.is_authenticated():
        context['profile'] = request.user.get_profile()

    return render_to_response(request, 'bus.html', context)


@login_required
def food(request):
    if request.POST:
        form = FoodForm(request.POST, profile=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('food') + '?save=ok')
    else:
        form = FoodForm(profile=request.user.get_profile())

    context = {
        'form': form,
        'save': request.GET.get('save'),
        'cost': [day[1] for day in settings.FOOD_DAYS],
    }

    return render_to_response(request, 'food.html', context)

############################################################################
# Reports

@permission_required('add_user')
def reports(request):
    return render_to_response(request, 'reports/index.html',
                              {'emails':", ".join(user.email for user in User.objects.all()),
                               'locked_roles_amount': Role.objects.filter(profile__isnull=False).count(),
                              })

@permission_required('add_user')
def report_contacts(request):
    return render_to_response(request, 'reports/contacts.html',
                          {'profiles': Profile.objects.all().filter(role__isnull=False, locked_fields__contains='role').order_by('role__order')}
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


@permission_required('add_user')
def report_food(request):
    table = []
    profiles = list(Profile.objects.exclude(food='0'*8))

    table.append([''] + [day[0] for day in settings.FOOD_DAYS] + [''])
    for profile in profiles:
        table.append([profile.name] + \
                     ['V' if profile.food[number] == '1' else '' for number in xrange(len(settings.FOOD_DAYS))] + \
                     [sum(settings.FOOD_DAYS[number][1] if profile.food[number] == '1' else 0 for number in xrange(len(settings.FOOD_DAYS)))]
        )

    table.append(
        [u"Итого"] + \
        [sum(int(profile.food[number]) for profile in profiles) for number in xrange(len(settings.FOOD_DAYS))] + \
        [sum(row[-1] and row[-1] or 0 for row in table)]
    )

    return render_to_response(request, 'reports/food.html', {'table': table})


def excel_report(func):
    def wrapper(request):
        context = func(request)
        if request.GET.get('mode') == 'xls':
            import xlwt
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet('sheet')

            for i, header in enumerate(context['headers']):
                sheet.write(0, i, header)

            for x, row in enumerate(context['rows']):
                for y, cell in enumerate(row):
                    sheet.write(x + 1, y, cell)

            wbk.save(settings.TMP_FILE)
            response = HttpResponse(open(settings.TMP_FILE, 'rb').read(), mimetype="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=report.xls'
            return response

        else:
            return render_to_response(request, 'reports/csv.html', context)

    return wrapper


@permission_required('add_user')
@excel_report
def report_bus(request):
    return {
        'title': u"Автобус",
        'headers': [u"ФИО", u"Ник", u"Телефон", u"Город",],
        'rows': [(role.profile.name, role.profile.user.username, role.profile.tel, role.profile.city)
        for role in Role.objects.filter(profile__isnull=False, profile__bus=True).order_by('profile__name').select_related('profile')]
    }


@permission_required('add_user')
def report_full(request):
    profiles = Profile.objects.filter(role__isnull=False, locked_fields__contains='role').order_by('name').select_related('role')
    if request.GET.get('n'):
        profiles = profiles[:int(request.GET.get('n'))]
    if request.GET.get('id'):
        profiles = profiles.filter(pk=int(request.GET.get('id')))

    for profile in profiles:
        profile.connections = list(RoleConnection.objects.filter(role=profile.role))
        profile.layers = list(LayerConnection.objects.filter(role=profile.role))
        profile.additional_info = profile.connections or profile.layers

    return render_to_response(request, 'reports/full.html',
        {'profiles': profiles}
    )



def rooms(request):
    context = {
        'available_rooms': Room.objects.filter(capacity__gt=F('current')),
        'profiles': Profile.objects.filter(room__isnull=False).order_by('room__title')
        }

    if request.user.is_authenticated():
        context['profile'] = request.user.get_profile()
        context['can_reserve'] = not context['profile'].is_locked('room')

    context['can_reserve'] = False  # Поселение окончено

    if context['can_reserve'] and request.POST and request.user.is_authenticated() \
            and not request.user.get_profile().is_locked('room'):
        room_id = int(request.POST['room'])
        try:
            room = Room.objects.get(pk=room_id)
            if room.available:
                profile = request.user.get_profile()
                profile.room = room
                profile.save()

                Room.recalc()
                return HttpResponseRedirect(reverse('rooms') + '?save=ok')

            else:
                context['message'] = u"Извините, выбранная вами комната уже заполнена."

        except Room.DoesNotExist:
            context['message'] = u"Нет такой комнаты."

    return render_to_response(request, 'rooms.html', context)
