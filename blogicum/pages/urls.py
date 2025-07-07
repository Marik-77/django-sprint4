"""Переадресация запросов
Импорты: функций path и views. В urlpatterns указываюся какие запросы
переадресовываются во views функции. Для удобства каждому URL указывается имя
name, которое будет использовано в ссылках html шаблонов. Так же указано
пространство имен app_name, чтобы определять к какому приложению относится
name.
"""
from django.urls import path

from pages import views

app_name = 'pages'
urlpatterns = [
    path('about/', views.AboutPage.as_view(), name='about'),
    path('rules/', views.RulesPage.as_view(), name='rules'),
]
