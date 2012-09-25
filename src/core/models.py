# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from yafotki.fields import YFField

from .utils import email


class GenericManager( models.Manager ):
    """
    Filters query set with given selectors
    """
    def __init__(self, **kwargs):
        super( GenericManager, self ).__init__()
        self.selectors = kwargs

    def get_query_set(self):
        return super( GenericManager, self ).get_query_set().filter( **self.selectors )


class RoleSection(models.Model):
    title = models.CharField(max_length=200, verbose_name=u"Название")
    order = models.IntegerField(verbose_name=u"Порядок", default=100)

    def __unicode__(self): return self.title

    class Meta:
        verbose_name = u"Раздел ролей"
        verbose_name_plural = u"Разделы ролей"
        ordering = ('order',)


class Role(models.Model):
    rolesection = models.ForeignKey(RoleSection, verbose_name=u"Раздел")
    name = models.CharField(max_length=200, verbose_name=u"ФИО")
    profession = models.CharField(max_length=200, verbose_name=u"Профессия")
    description = models.TextField(verbose_name=u"Описание", null=True, blank=True)
    cache = models.IntegerField(verbose_name=u"Наличность", default=0)
    account = models.IntegerField(verbose_name=u"Деньги на счете", default=0)

    order = models.IntegerField(verbose_name=u"Порядок", default=10000)
    profile = models.ForeignKey('Profile', verbose_name=u'Профиль', null=True, blank=True, related_name="locked_role")

    def __unicode__(self): return self.name

    class Meta:
        verbose_name = u"Роль"
        verbose_name_plural = u"Роли"
        ordering = ('order',)


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь', null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name=u"ФИО", null=True, blank=True)
    age = models.IntegerField(verbose_name=u"Возраст", null=True, blank=True)
    city = models.CharField(max_length=200, verbose_name=u"Город", null=True, blank=True)
    icq = models.CharField(max_length=200, verbose_name=u"ICQ", null=True, blank=True)
    tel = models.CharField(max_length=200, verbose_name=u"Телефон", null=True, blank=True)
    med = models.CharField(max_length=200, verbose_name=u"Медицинские особенности", null=True, blank=True)

    gun = models.CharField(max_length=200, verbose_name=u"Оружие", null=True, blank=True)
    goal = models.TextField(verbose_name=u"Цель")
    dream = models.TextField(verbose_name=u"Мечта", null=True, blank=True)
    portrait = YFField(
        verbose_name=u"Фото",
        upload_to='sincity',
        null=True, blank=True, default=None,
    )

    role = models.ForeignKey(Role, verbose_name=u"Роль", null=True, blank=True, related_name="suggested_role")
    quest = models.TextField(verbose_name=u'Квента', null=True, blank=True, default=None)

    paid = models.BooleanField(verbose_name=u"Взнос внесен", default=False)
    special = models.TextField(verbose_name=u'Спец. способности', null=True, blank=True, default=None)
    bus = models.BooleanField(verbose_name=u"Поедет автобусом", default=False)
    food = models.CharField(verbose_name=u"Питание", max_length=8, default='0'*8)
    room = models.ForeignKey('Room', verbose_name=u"Комната", null=True, blank=True, default=None)

    locked_fields = models.CharField(max_length="300", verbose_name=u"Замороженные поля", null=True, blank=True)

    def __unicode__(self): return self.user.username

    def form_link(self):
        return "<a href='" + reverse('form') + '?change_user=%s' % self.user.id + "'>анкета</a>"
    form_link.short_description = u"Анкета"
    form_link.allow_tags = True

    def user_email(self):
        return self.user.email
    user_email.short_description = u"Email"

    def user_username(self):
        return self.user.username
    user_username.short_description = u"Ник"

    def role_locked(self):
        if not self.role:
            return ''
        return self.role.profile == self and '+' or ''
    role_locked.short_description = u"Роль заморожена"

    def is_locked(self, field):
        return self.locked_fields and field in self.locked_fields

    def lock(self, field):
        if not self.locked_fields:
            self.locked_fields = ''
        if not self.is_locked(field):
            fields = self.locked_fields.split(',')
            fields.append(field)
            self.locked_fields = ",".join(fields)
            self.save()

            if field == 'role':
                self.role.profile = self
                self.role.save()

    def unlock(self, field):
        if not self.locked_fields:
            self.locked_fields = ''
        if self.is_locked(field):
            fields = self.locked_fields.split(',')
            fields.append(field)
            self.locked_fields = ",".join([f for f in fields if f != field])
            self.save()

            if field == 'role':
                self.role.profile = None
                self.role.save()


    def save(self, check_diff=True, *args, **kwargs):
        if self.pk and check_diff:
            prev = self.__class__.objects.get(pk=self.pk)
            report = ""
            for field in self._meta.fields:
                if field.name in('paid', 'locked_fields'):
                    continue

                if getattr(self, field.name) != getattr(prev, field.name):
                    report += u"%s: '%s' -> '%s'\n" % (field.verbose_name, getattr(prev, field.name) or '-', getattr(self, field.name) or '-')

            if report:
                email(
                    u"SinCity 2012: изменения в профиле игрока %s" % self.name,
                    u"Измененные поля профиля [http://sincity2012.ru/form?change_user=%s]:\n%s" % (self.user.pk, report),
                    [self.user.email],
                )

        return super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Профиль"
        verbose_name_plural = u"Профили"


class RoleConnection(models.Model):
    role = models.ForeignKey(Role, verbose_name=u"Роль", related_name='roles')
    role_rel = models.ForeignKey(Role, verbose_name=u"Связанная роль", related_name='linked_roles', null=True, blank=True)
    comment = models.TextField(verbose_name=u"Описание", null=True, blank=True, default=None)
    is_locked = models.BooleanField(verbose_name=u"Заморожено", default=False)

    def save(self, *args, **kwargs):
        if self.role.profile:
            emails = [self.role.profile.user.email]
        else:
            emails = []

        if self.pk:
            prev = self.__class__.objects.get(pk=self.pk)
            if getattr(self, 'comment') != getattr(prev, 'comment'):
                report = u"Анкета: http://sincity2012.ru/form?change_user=%s\n\nИзмененная связь: %s -> %s:\nБыло: %s\nСтало: '%s'" % \
                         (self.role.profile.user.pk, self.role,
                          self.role_rel, getattr(prev,'comment') or '-', getattr(self, 'comment') or '-')

                email(
                    u"SinCity 2012: изменения в связях роли %s" % self.role,
                    report,
                    emails,
                )
        else:
            if self.role.profile:
                profile = self.role.profile
            else:
                profile = Profile.objects.filter(role=self.role)[0]

            email(u"SinCity 2012: новая связь между ролями",
                u"Анкета: http://sincity2012.ru/form?change_user=%s\n\n%s -> %s\n\n%s"
                % (profile.user.pk, self.role, self.role_rel, self.comment),
                emails,
            )

        return super(RoleConnection, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Связь ролей"
        verbose_name_plural = u"Связи ролей"


class Layer(models.Model):
    title = models.CharField(verbose_name=u"Название", max_length=200)

    def __unicode__(self): return self.title

    class Meta:
        verbose_name = u"Пласт"
        verbose_name_plural = u"Пласты"


class LayerConnection(models.Model):
    role = models.ForeignKey(Role, verbose_name=u"Роль")
    layer = models.ForeignKey(Layer, verbose_name=u"Пласт", related_name='roles')
    comment = models.TextField(verbose_name=u"Описание", null=True, blank=True, default=None)
    is_locked = models.BooleanField(verbose_name=u"Заморожено", default=False)

    def save(self, *args, **kwargs):
        emails = []
        if self.role and self.role.profile:
            emails.append(self.role.profile.user.email)
        if self.layer_id == 6:
            emails.append('linashyti@gmail.com')  # мастер по пласту "наука"

        if self.pk:
            prev = self.__class__.objects.get(pk=self.pk)
            if getattr(self, 'comment') != getattr(prev, 'comment'):
                report = u"Измененный пласт: %s -> %s:\nБыло: %s\nСтало: '%s'" % (self.role, self.layer, getattr(prev,'comment') or '-', getattr(self, 'comment') or '-')

                email(
                    u"SinCity 2012: изменения в пласте роли %s" % self.role,
                    report,
                    emails,
                )
        else:
            email(
                u"SinCity 2012: новый пласт роли %s" % self.role,
                u"%s -> %s\n\n%s" % (self.role, self.layer, self.comment),
                emails,
            )

        return super(LayerConnection, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Связь с пластом"
        verbose_name_plural = u"Связи с пластами"


class Gallery(models.Model):
    title = models.CharField(max_length=200, verbose_name=u"Название")

    class Meta:
        verbose_name = u"Галерея"
        verbose_name_plural = u"Галереи"


class News(models.Model):
    date_created = models.DateField(verbose_name=u"Дата публикации", null=True, blank=True, default=None)
    title = models.CharField(verbose_name=u"Заголовок", max_length=50)
    content = models.TextField(verbose_name=u"Содержание")

    def __unicode__(self): return self.title

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.now()

        super(News, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"
        ordering = ('-date_created',)


class Article(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, default=None)
    title = models.CharField(verbose_name=u"Заголовок", max_length=50)
    content = models.TextField(verbose_name=u"Содержание")
    order = models.PositiveSmallIntegerField(verbose_name=u"Порядок", default=100)
    redirect = models.CharField(verbose_name=u"Редирект", max_length=50, null=True, blank=True, default=None)
    path = models.CharField(verbose_name=u"Путь", max_length=50, default="", blank=True)

    def __unicode__(self): return self.title

    def save(self, *args, **kwargs):
        if not self.path:
            if self.parent:
                above_amount = Article.objects.filter(parent=self.parent).count()
                self.path = self.parent.path + "%02d" % (above_amount + 1)
            else:
                above_amount = Article.objects.filter(parent__isnull=True).count()
                self.path = "%02d" % (above_amount + 1)

        super(Article, self).save(*args, **kwargs)

    def indent_title(self):
        return u'&nbsp' * len(self.path) + self.title
    indent_title.short_description = u"Название"
    indent_title.allow_tags = True

    class Meta:
        verbose_name = u"Страница"
        verbose_name_plural = u"Страницы"
        ordering = ('order',)


class Room(models.Model):
    floor = models.CharField(max_length=200, verbose_name=u"Этаж", default=u"-")
    title = models.CharField(max_length=200, verbose_name=u"Название", default=u"-")
    capacity = models.PositiveIntegerField(verbose_name=u"Вместимость", default=2)
    current = models.PositiveIntegerField(verbose_name=u"Наполненность", default=0)

    def __unicode__(self):
        return self.title

    @property
    def available(self):
        return self.capacity > self.current

    @classmethod
    def recalc(cls):
        rooms = dict((room.id, 0) for room in cls.objects.all())
        for profile in Profile.objects.filter(room__isnull=False):
            rooms[profile.room_id] = rooms.get(profile.room_id, 0) + 1

        for id, amount in rooms.items():
            cls.objects.filter(pk=id).update(current=amount)

    class Meta:
        verbose_name = u"Комната"
        verbose_name_plural = u"Комнаты"
        ordering = ('title',)


def change_user_link(self):
    return "<a href='" + reverse('change_user', args=[self.id]) + "'>сменить пользователя</a>"
change_user_link.short_description = u"Сменить пользователя"
change_user_link.allow_tags = True

User.change_user_link = change_user_link