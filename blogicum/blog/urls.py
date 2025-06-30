"""Переадресация запросов
Импорты: функций path и views. В urlpatterns указываюся какие запросы
переадресовываются во views функции. Для удобства каждому URL указывается имя
name, которое будет использовано в ссылках html шаблонов. Так же указано
пространство имен app_name, чтобы определять к какому приложению относится
name.

<int:id> - означает что id целое число; пример запроса: posts/2/

<slug:category_slug> - означает что category_slug состоит из простых символов и
цифр; пример запроса: posts/some-t-1/.
"""


from blog import views
from django.contrib.auth import get_user_model
from django.urls import path

User = get_user_model()

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('profile/<slug:username>/', views.ProfileView.as_view(),
         name='profile'),
    path('category/<slug:category_slug>/',
         views.CategoryPostsView.as_view(), name='category_posts'),

    path('profile/<int:post_id>/edit/',
         views.EditProfilView.as_view(), name='edit_profile'),

    path('posts/<int:post_id>/', views.PostDetailView.as_view(),
         name='post_detail'),



    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),

    path('posts/<int:post_id>/comment/', views.add_comment,
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.EditComment.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.DeleteComment.as_view(), name='delete_comment'),
]
