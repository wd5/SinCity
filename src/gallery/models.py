# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, mail_managers

from yafotki.fields import YFField

class Gallery(models.Model):
    title = models.CharField(max_length=200, verbose_name=u"Название")

    class Meta:
        verbose_name = u"Галерея"
        verbose_name_plural = u"Галереи"


class Photo(models.Model):
    gallery = models.ForeignKey(Gallery, verbose_name=u"Галерея")
    title = models.CharField(max_length=200, verbose_name=u"Название", null=True, blank=True, default=None)
    img = YFField(
        verbose_name=u"Фото",
        upload_to='sincity',
        null=True, blank=True, default=None,
    )

    class Meta:
        verbose_name = u"Фотография"
        verbose_name_plural = u"Фотографии"