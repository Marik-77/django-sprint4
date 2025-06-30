"""Обработка запросов статичных страниц about и rules
about - страница с информацией о проекте, rules - страница правилами для
пользователей.
"""

from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    """Обработка страницы с информацией о проекте."""

    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    """Обработка страницы с правилами для пользователей."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Ошибка для страницы 404."""
    return render(request, 'pages/404.html', status=404)


def page_csrf_failure(request, reason=''):
    """Ошибка для страницы 403 CSRF."""
    return render(request, 'pages/403csrf.html', status=403)


def page_server_error(request):
    """Ошибка для страницы 500."""
    return render(request, 'pages/500.html', status=500)
