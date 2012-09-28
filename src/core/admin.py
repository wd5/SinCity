# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class ProfileAdmin(admin.ModelAdmin):
   list_display = ('user', 'name', 'user_username', 'user_email', 'tel', 'city', 'role', 'role_locked', 'form_link', 'print_link')

   def lookup_allowed(self, *args, **kwargs):
       return True

class RoleSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

class RoleAdmin(admin.ModelAdmin):
   list_display = ('name', 'rolesection', 'profession', 'profile')
   raw_id_fields = ('profile',)


class RoleConnectionAdmin(admin.ModelAdmin):
   list_display = ('role', 'role_rel', 'is_locked')


class LayerConnectionAdmin(admin.ModelAdmin):
   list_display = ('layer', 'role', 'is_locked')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'title', 'content')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('indent_title', 'order', 'path')
    actions = ['recalc_paths']
    ordering = ('path',)

    def recalc_paths(self, request, queryset):
        for number, article in enumerate(Article.objects.filter(parent__isnull=True).order_by('order')):
            article.path = "%02d" % (number + 1)
            article.save()

            self._recalc_article_children(article)
    recalc_paths.short_description = u"Пересчитать порядок"

    def _recalc_article_children(self, article):
        for number, child in enumerate(Article.objects.filter(parent=article).order_by('order')):
            child.path = article.path + "%02d" % (number + 1)
            child.save()
            self._recalc_article_children(child)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'capacity', 'current')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(RoleSection, RoleSectionAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(RoleConnection, RoleConnectionAdmin)
admin.site.register(Layer)
admin.site.register(LayerConnection, LayerConnectionAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Room, RoomAdmin)
