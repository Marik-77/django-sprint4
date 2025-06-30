"""Кастомная модель пользователя"""
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    """Переопределена стандартная модель. Есть возможность изменять ее в
    будущем
    """

    pass
