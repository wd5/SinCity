# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Gallery, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 5


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = (PhotoInline,)

admin.site.register(Gallery, GalleryAdmin)