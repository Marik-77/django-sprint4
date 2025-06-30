from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма для создания пользователя.
    Наследуется от стандартной формы, изменяет модель пользователя на
    кастомную.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    """Кастомная форма для изменения пользователя.
    Наследуется от стандартной формы, изменяет модель пользователя на
    кастомную.
    """

    password = None

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
