# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate
from django.forms import *
from django.db.models import Q
from django.conf import settings

from models import *
from .utils import email

class CommonForm(Form):
    def errors_list(self):
        return [u"%s: %s" % (self.fields[_].label, message) for _, l in self.errors.items() for message in l]

    def str_errors(self, divider=u" "):
        return divider.join(self.errors_list())


class RegistrationForm(CommonForm):
    login = CharField(label=u'Ник', max_length=100)
    passwd = CharField(label=u'Пароль', max_length=100, widget=PasswordInput)
    email = EmailField(label=u'Email', max_length=100)

    def save(self):
        new_user = User.objects.create_user(self.cleaned_data['login'],
                                            self.cleaned_data['email'],
                                            self.cleaned_data['passwd'])
        new_user.is_active = True
        new_user.save()

        return authenticate(username=new_user.username, password=self.cleaned_data['passwd'])


class LoginForm(CommonForm):
    login = CharField(label=u'Ник', max_length=100)
    passwd = CharField(label=u'Пароль', max_length=100, widget=PasswordInput)
    retpath = CharField(max_length=2000, required=False, widget=HiddenInput)

    def get_user(self, s):
        u""" Проверяет строку на емейл, логин или имя пользователя """
        return User.objects.get(Q(username=s)|Q(email=s)|Q(first_name=s))

    def clean(self):
        login = self.cleaned_data.get('login', '')
        passwd = self.cleaned_data.get('passwd', '')

        try:
            user = self.get_user(login)
        except User.DoesNotExist:
            raise ValidationError(u'Логин или пароль не верен')

        auth_user = authenticate(username=user.username, password=passwd)
        if auth_user:
            self.user = auth_user
            return self.cleaned_data
        else:
            raise ValidationError(u'Логин или пароль не верен')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'locked_fields', 'food', 'bus', 'paid', 'room')

    name = CharField(label=u'ФИО персонажа', max_length=200, widget=TextInput(attrs={'size':'60'}), required=False)
    med  = CharField(label=u'Мед. показатели', max_length=200, widget=TextInput(attrs={'size':'60'}), required=False)
    gun  = CharField(label=u'Оружие', max_length=200, widget=TextInput(attrs={'size':'40'}), required=False)
    goal = CharField(label=u'Цель', max_length=200, widget=Textarea(attrs={'rows':'4', 'cols':'40'}), required=False)
    dream = CharField(label=u'Мечта', max_length=200, widget=Textarea(attrs={'rows':'4', 'cols':'40'}), required=False)
    quest = CharField(label=u'Квента', max_length=20000, widget=Textarea(attrs={'rows':'15', 'cols':'100'}), required=False)

    role = IntegerField(label=u'Роль', required=False, widget=Select)

    role_name = CharField(label=u'Имя персонажа', required=False, max_length=200, widget=TextInput(attrs={'size':'40'}))
    role_profession = CharField(label=u'Профессия персонажа', required=False, max_length=200, widget=TextInput(attrs={'size':'40'}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.roles = list(Role.objects.filter(profile__isnull=True).order_by('rolesection__order', 'order'))

        if 'instance' in kwargs:
            if kwargs['instance'].role_id:
                self.roles.insert(0, kwargs['instance'].role)

            self.initial['role'] = kwargs['instance'].role_id or Role.objects.all()[0].id
            role = Role.objects.get(pk=self.initial['role'])
            self.initial['role_name'] = role.name
            self.initial['role_profession'] = role.profession

            if kwargs['instance'].role_id:
                for field in ('role_name', 'role_profession'):
                    self.fields[field].widget.attrs['disabled'] = 'disabled'

            for field in self.fields.keys():
                if kwargs['instance'].is_locked(field):
                    del self.fields[field]

        if 'role' in self.fields:
            self.fields['role'].widget.choices = [(role.pk, u"%s, %s" % (role.name, role.profession)) \
                                                            for role in self.roles]
            self.fields['role'].widget.choices.append((0, u'-- своя роль --'))


    def clean_role(self, *args, **kwargs):
        if 'role' in self.fields.keys() and self.cleaned_data['role'] is None:
            return self.initial['role']

        if int(self.cleaned_data['role']) == 0 and not \
            (self.data.get('role_name') or self.data.get('role_profession')):
            raise ValidationError(u"Заполните поля роли, чтобы создать ее")

        return int(self.cleaned_data['role'])


    def clean(self):
        if self._errors:
            self.cleaned_data['role'] = None
            return self.cleaned_data

        if 'role' in self.fields:
            if self.cleaned_data['role'] == 0:
                role = Role.objects.create(name=self.cleaned_data['role_name'],
                                           profession=self.cleaned_data['role_profession'],
                                           description='',
                                           rolesection=RoleSection.objects.get(pk=7),
                                           )

            else:
                role = Role.objects.get(pk=self.cleaned_data['role'])

            self.cleaned_data['role'] = role

        return super(ProfileForm, self).clean()


    def errors_list(self):
        return [u"%s: %s" % (field == '__all__' and u'Общая ошибка' or self.fields[field].label, message) for field, l in self.errors.items() for message in l]

    def str_errors(self, divider=u" "):
        return divider.join(self.errors_list())


class FoodForm(CommonForm):
    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile')
        super(FoodForm, self).__init__(*args, **kwargs)

        for number, checkbox in enumerate(settings.FOOD_DAYS):
            self.fields['field_%s' % number] = forms.BooleanField(label=checkbox[0], required=False, help_text=u"%s руб." % checkbox[1])

        self.profile = profile
        for number, checkbox in enumerate(settings.FOOD_DAYS):
            self.initial['field_%s' % number] = profile.food[number] == '1' and True or False

    def save(self):
        self.profile.food = "".join(self.cleaned_data['field_%s' % number] and '1' or '0' for number in xrange(len(settings.FOOD_DAYS)))
        self.profile.save()


from django.forms.models import inlineformset_factory
ConnectionFormSet = inlineformset_factory(Role, RoleConnection, fk_name="role", exclude=('is_locked',), extra=1)
LayerFormSet = inlineformset_factory(Role, LayerConnection, fk_name="role", exclude=('is_locked',), extra=1)


import datetime
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.contrib.auth.models import User

from messages.models import Message

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient = forms.CharField(label=_(u"Recipient"), widget=Select)
    subject = forms.CharField(label=_(u"Subject"))
    body = forms.CharField(label=_(u"Body"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))


    def __init__(self, *args, **kwargs):
        super(ComposeForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].widget.choices = [(role.pk, role.name)\
            for role in Role.objects.filter(profile__isnull=False).order_by('name')]


    def save(self, sender, parent_msg=None):
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        role = Role.objects.get(pk=self.cleaned_data['recipient'])
        user = role.profile.user
        msg = Message(
            sender = sender,
            recipient = user,
            subject = subject,
            body = body,
        )
        if parent_msg is not None:
            msg.parent_msg = parent_msg
            parent_msg.replied_at = datetime.datetime.now()
            parent_msg.save()
        msg.save()
        message_list.append(msg)

        email(
            u"SinCity2012: новое сообщение в личных",
            u"Вам было послано сообщение. Вы можете прочитать его по ссылке http://%s%s" % (settings.DOMAIN, reverse('messages_inbox')),
            [user.email],
            admins=False,
        )
        return message_list
