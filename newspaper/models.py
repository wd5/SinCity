# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse


class Post(models.Model):
    NEWSPAPER = (
        (1, u'Daily Bugle'),
    )
    newspaper = models.IntegerField(choices=NEWSPAPER, default=1, verbose_name=u"Газета")
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, verbose_name=u"Заголовок")
    image = models.ImageField(upload_to='data', verbose_name=u"Картинка")
    content = models.TextField(verbose_name=u"Содержание")

    def __unicode__(self):
        return u"%s: %s" % (self.get_newspaper_display(), self.title)

    def get_absolute_url(self):
        return reverse('post', args=[self.pk])

    class Meta:
        verbose_name = u"Выпуск"
        verbose_name_plural = u"Выпуски"
        ordering = ('-date_created',)
