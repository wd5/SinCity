# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib.auth.views import password_reset

from views import *
from models import News

urlpatterns = patterns('',
    url(r'^roles$', roles, name='roles'),
    url(r'^form', request_form, name='form'),
    url(r'^lock$', lock, name='lock'),
    url(r'^lock_rel$', lock_rel, name='lock_rel'),
    url(r'^news$', list_detail.object_list, {"queryset": News.objects.all()[5:]}, name='news'),
    url(r'^article/(?P<object_id>\d+)$', list_detail.object_detail, {'queryset': Article.objects.all()}, name='article'),
    url(r'^bus', bus, name='bus'),
    url(r'^food', food, name='food'),
    url(r'^rooms', rooms, name='rooms'),

    url(r'^reports/$', reports),
    url(r'^reports/contacts/$', report_contacts),
    url(r'^reports/paid/$', report_paid),
    url(r'^reports/layers/$', report_layers),
    url(r'^reports/players_without_roles/$', report_players_without_roles),
    url(r'^reports/food/$', report_food, name='report_food'),
    url(r'^reports/bus/$', report_bus, name='report_bus'),
    url(r'^reports/money/$', report_money, name='report_money'),
    url(r'^reports/full/$', report_full, name='report_full'),

    url(r'^$', index , name='index'),
    )