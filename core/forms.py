# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.forms import *
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.db.models import Q

from models import *

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
        exclude = ('user', 'locked_fields')

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
        #print "START", ",".join(self.fields.keys())

        self.roles = list(Role.objects.filter(profile__isnull=True).order_by('section', 'order'))

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
                                           )

            else:
                role = Role.objects.get(pk=self.cleaned_data['role'])

            self.cleaned_data['role'] = role

        return super(ProfileForm, self).clean()


    def errors_list(self):
        return [u"%s: %s" % (field == '__all__' and u'Общая ошибка' or self.fields[field].label, message) for field, l in self.errors.items() for message in l]

    def str_errors(self, divider=u" "):
        return divider.join(self.errors_list())


from django.forms.models import inlineformset_factory
ConnectionFormSet = inlineformset_factory(Role, RoleConnection, fk_name="role", exclude=('is_locked',), extra=1)
LayerFormSet = inlineformset_factory(Role, LayerConnection, fk_name="role", exclude=('is_locked',), extra=1)
