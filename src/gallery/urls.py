# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from .views import gallery

urlpatterns = patterns('',
    url(r'^(\d+)$', gallery, name='gallery'),
    )
