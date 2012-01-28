# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from core.models import RoleConnection, News

register = template.Library()

@register.simple_tag
def MEDIA_URL():
    return settings.MEDIA_URL


@register.inclusion_tag('lock_buttons.html')
def locker(field, form, is_superuser):
    if not hasattr(form, 'instance') or not is_superuser:
        return {}

    return {'field': field, 'locked': form.instance.is_locked(field)}


@register.inclusion_tag('lock_buttons_rel.html')
def locker_rel(rel, form, is_superuser):
    if (form and not hasattr(form, 'instance')) or not is_superuser:
        return {}

    return {'rel': rel, 'locked': rel.is_locked}


@register.inclusion_tag('locked_connections.html')
def locked_connections(profile, is_superuser):
    return {'connections': RoleConnection.objects.filter(role=profile.role, is_locked=True), 'is_superuser': is_superuser}


@register.filter
def br(text):
    return mark_safe(text.replace("\n", "<br>\n"))


@register.inclusion_tag('last_news.html')
def last_news():
    news = News.objects.all().order_by('-date_created')[:5]
    return {'news': news}