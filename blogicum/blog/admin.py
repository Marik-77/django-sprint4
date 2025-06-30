"""Админ-зона.
Модели импортируются. Создается собственный класс, унаследованный от
admin.ModelAdmin, в унаследованном классе переопределяются настройки интерфейса
админки. Модели регистрируются для отображения в админ-зоне.
"""


from django.contrib import admin

from .models import Category, Comment, Location, Post


class PostAdmin(admin.ModelAdmin):
    """Отображение модели Post.
    list_display - поля которые будут отображаться;
    list_editable - редактируемые поля; search_fields - поиск по полю;
    list_filter - фильтр; list_display_links - ссылка переход.
    """

    list_display = (
        'title',
        'created_at',
        'is_published',
        'pub_date',
        'author',
        'location',
        'category'
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    """Отображение модели Category."""

    list_display = (
        'title',
        'slug',
        'created_at',
        'is_published'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)


class LocationAdmin(admin.ModelAdmin):
    """Отображение модели Location."""

    list_display = (
        'name',
        'created_at'
    )
    search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
    """Отображение модели Comment."""

    list_display = (
        'text',
        'author',
        'created_at',
        'post'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
