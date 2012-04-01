# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template import RequestContext, Context, loader

from models import Post

def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict or {})
    return _render_to_response(template_name, context_instance=context)


def newspaper(request, newspaper_id):
    return render_to_response(request, 'newspaper/newspaper.html',
                              {'posts': Post.objects.filter(newspaper=newspaper_id)}
                              )