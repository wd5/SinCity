# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import get_object_or_404

from .models import Gallery, Photo


def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict or {})
    return _render_to_response(template_name, context_instance=context)


def gallery(request, gallery_id):
    return render_to_response(
        request,
        'gallery/gallery.html',
        {
            'gallery': get_object_or_404(Gallery, pk=gallery_id),
            'photos': Photo.objects.filter(gallery=gallery_id),
        }
    )

