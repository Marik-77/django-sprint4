"""Регистрация модели пользователей в админке"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser


class MyUserAdmin(UserAdmin):
    """Кастомный UserAdmin с отображением количества постов."""

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Количество постов'

    list_display = UserAdmin.list_display + ('post_count',)

admin.site.register(MyUser, MyUserAdmin)

