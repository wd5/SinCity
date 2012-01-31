# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class ProfileAdmin(admin.ModelAdmin):
   list_display = ('user', 'name', 'user_username', 'user_email', 'tel', 'city', 'role', 'role_locked', 'form_link')

   def lookup_allowed(self, *args, **kwargs):
       return True


class RoleAdmin(admin.ModelAdmin):
   list_display = ('name', 'section', 'profession', 'profile')
   raw_id_fields = ('profile',)


class RoleConnectionAdmin(admin.ModelAdmin):
   list_display = ('role', 'role_rel', 'is_locked')


class LayerConnectionAdmin(admin.ModelAdmin):
   list_display = ('layer', 'role', 'is_locked')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'title', 'content')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(RoleConnection, RoleConnectionAdmin)
admin.site.register(Layer)
admin.site.register(LayerConnection, LayerConnectionAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Article, ArticleAdmin)