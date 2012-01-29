# -*- coding: utf-8 -*-
from hashlib import md5
import os
import Image
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, mail_managers

from south.modelsinspector import add_introspection_rules


class ThumbnailImageFieldFile(models.fields.files.ImageFieldFile):
    def get_thumbnail(self):
        u""" Возвращает tuple (урл, (размеры))"""
        if not self.name:
            return "",(0, 0)

        ext = self.name.split('.')[-1]
        thumbnail_file = md5(self.name.encode('utf8')).hexdigest() + '.' + ext
        thumbnail_dir = thumbnail_file[0:2]
        thumbnail_path = os.path.join(settings.THUMBNAIL_ROOT, thumbnail_dir, thumbnail_file)
        if os.path.exists(thumbnail_path):
            try:
                im = Image.open(thumbnail_path)
                return "%s%s/%s" % (settings.THUMBNAIL_URL, thumbnail_dir, thumbnail_file), im.size
            except IOError:
                return "%s%s/%s" % (settings.THUMBNAIL_URL, thumbnail_dir, thumbnail_file), (0, 0)


        file = os.path.join(settings.MEDIA_ROOT, self.name)
        if not os.path.exists(file):
            open(settings.WARNING_LOG_PATH, 'a').write("file '%s' not found\n" % self.name)
            return "[file '%s' not found]" % self.name, (0, 0)

        if not os.path.exists(os.path.join(settings.THUMBNAIL_ROOT, thumbnail_dir)):
            os.mkdir(os.path.join(settings.THUMBNAIL_ROOT, thumbnail_dir))

        try:
            #FIXME: сделать генерацию тумбнейлов отдельным Thread
            im = Image.open(file)
            im.thumbnail(settings.THUMBNAIL_SIZE, Image.ANTIALIAS)
            im.save(os.path.join(settings.THUMBNAIL_ROOT, thumbnail_dir, thumbnail_file))
            return "%s%s/%s" % (settings.THUMBNAIL_URL, thumbnail_dir, thumbnail_file), im.size

        except IOError, e:
            return "cannot create thumbnail for %s: %s" % (self.name, e), (0, 0)

    def get_thumbnail_url(self):
        return self.get_thumbnail()[0]


class ThumbnailImageField(models.ImageField):
    attr_class = ThumbnailImageFieldFile

rules = [(
            (ThumbnailImageField, ),
            [],
            {},
        ),]

add_introspection_rules(rules, ["^core",])


class GenericManager( models.Manager ):
    """
    Filters query set with given selectors
    """
    def __init__(self, **kwargs):
        super( GenericManager, self ).__init__()
        self.selectors = kwargs

    def get_query_set(self):
        return super( GenericManager, self ).get_query_set().filter( **self.selectors )

SECTIONS = (('policy', u"Полиция"),
            ('med', u'Медицина'),
            ('politics', u'Политика и экономика'),
            ('religion', u'Религия'),
            ('jounalist', u'Журналистика'),
            ('porn', u'Бордель и иже с ними'),
            ('other', u'Остальные граждане города'),
)

class Role(models.Model):
    section = models.CharField(max_length=20, verbose_name=u"Раздел", choices=SECTIONS, default='other')
    name = models.CharField(max_length=200, verbose_name=u"ФИО")
    profession = models.CharField(max_length=200, verbose_name=u"Профессия")
    description = models.TextField(verbose_name=u"Описание", null=True, blank=True)
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
    photo = ThumbnailImageField(upload_to='data', null=True, blank=True)

    role = models.ForeignKey(Role, verbose_name=u"Роль", null=True, blank=True, related_name="suggested_role")
    quest = models.TextField(verbose_name=u'Квента', null=True, blank=True, default=None)

    paid = models.BooleanField(verbose_name=u"Взнос внесен", default=False)
    special = models.TextField(verbose_name=u'Спец. способности', null=True, blank=True, default=None)
    bus = models.BooleanField(verbose_name=u"Поедет автобусом", default=False)

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
        if self.pk and check_diff and not settings.DEBUG:
            prev = self.__class__.objects.get(pk=self.pk)
            report = ""
            for field in self._meta.fields:
                if field.name in('paid', 'locked_fields'):
                    continue

                if getattr(self, field.name) != getattr(prev, field.name):
                    report += u"%s: '%s' -> '%s'\n" % (field.verbose_name, getattr(prev, field.name) or '-', getattr(self, field.name) or '-')

            if report:
                report = u"Измененные поля профиля [http://sincity2012.ru/form?change_user=%s]:\n" % self.user.pk + report
                emails = [settings.MANAGERS[0][1], settings.ADMINS[0][1], self.user.email]

                send_mail(u"SinCity 2012: изменения в профиле игрока %s" % self.name,
                            report,
                            settings.SERVER_EMAIL,
                            emails,
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
        if not settings.DEBUG:
            if self.pk:
                prev = self.__class__.objects.get(pk=self.pk)
                if getattr(self, 'comment') != getattr(prev, 'comment'):
                    report = u"Анкета: http://sincity2012.ru/form?change_user=%s\n\nИзмененная связь: %s -> %s:\nБыло: %s\nСтало: '%s'" % \
                             (self.role.profile.user.pk, self.role,
                              self.role_rel, getattr(prev,'comment') or '-', getattr(self, 'comment') or '-')
                    emails = [settings.MANAGERS[0][1], settings.ADMINS[0][1]]
                    if self.role.profile:
                        emails.append(self.role.profile.user.email)

                    send_mail(u"SInCity 2012: изменения в связях роли %s" % self.role,
                                report,
                                settings.SERVER_EMAIL,
                                emails,
                                )
            else:
                mail_managers(u"SinCity 2012: новая связь между ролями", "Анкета: http://sincity2012.ru/form?change_user=%s\n\n%s -> %s" % (self.role.profile.user.pk, self.role, self.role_rel))

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
        if not settings.DEBUG:
            if self.pk:
                prev = self.__class__.objects.get(pk=self.pk)
                if getattr(self, 'comment') != getattr(prev, 'comment'):
                    report = u"Измененный пласт: %s -> %s:\nБыло: %s\nСтало: '%s'" % (self.role, self.layer, getattr(prev,'comment') or '-', getattr(self, 'comment') or '-')
                    emails = [settings.MANAGERS[0][1], settings.ADMINS[0][1]]
                    if self.role.profile:
                        emails.append(self.role.profile.user.email)

                    send_mail(u"SinCity 2012: изменения в пласте роли %s" % self.role,
                                report,
                                settings.SERVER_EMAIL,
                                emails,
                                )
            else:
                mail_managers(u"SinCity 2012: новый пласт роли", "%s -> %s" % (self.role, self.layer))

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

    def __unicode__(self): return self.title

    class Meta:
        verbose_name = u"Страница"
        verbose_name_plural = u"Страницы"
        ordering = ('order',)