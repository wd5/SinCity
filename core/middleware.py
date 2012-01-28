from django.contrib.flatpages.views import flatpage
from django.http import Http404
from django.conf import settings

class Process404Middleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.
        else:
            return flatpage(request, '/404/')
