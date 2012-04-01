# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from newspaper.views import newspaper

urlpatterns = patterns('',       
    url(r'^(?P<newspaper_id>\d+)/$', newspaper, name='newspaper'),
    )
