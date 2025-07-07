"""blogicum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

В списке urlpatterns указываются адреса которые обрабатывает django. Добавлены
три адреса: 1) '' - главная страница переадресовывается в приложении blog;
2)'admin/' - панель администраторв 3) 'pages/' - дополнительные страницы,
которые переадресовываются в приложении pages; 4) 'auth/' - модуль
аутентификации. 5) 'auth/registration/' - страница регистрации пользователей.
Добавлены handler404 и handler500 - адрес view-функции с ошибками. Если включен
режим отладки, то подключаем toolbar и статику.
"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import UserCreationForm

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.page_server_error'

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
