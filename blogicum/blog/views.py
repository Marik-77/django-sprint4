"""Обработка запросов."""
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import Category, Post
from users.forms import UserChangeForm

from .forms import CommentForm, PostForm
from .mixins import CommentMixin, OnlyAuthorMixin
from .utils import sql_filters

NUMBER_OF_POSTS_PER_PAGE = 10
User = get_user_model()


@login_required
def add_comment(request, post_id):
    """Создание комментрария.
    Отображается на странице PostDetail.
    """
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


class EditComment(CommentMixin, OnlyAuthorMixin, UpdateView):
    """Изменение комментрария."""

    form_class = CommentForm


class DeleteComment(CommentMixin, OnlyAuthorMixin, DeleteView):
    """Удаление комментрария."""

    pass


def get_post_queryset():
    """Базовый запрос для постов с нужными select_related и аннотацией."""
    return sql_filters(
        Post.objects.select_related('category', 'location', 'author')
    ).annotate(comment_count=Count("comments"))


class PostListView(ListView):
    """Cтраница с постами."""

    paginate_by = NUMBER_OF_POSTS_PER_PAGE
    model = Post
    template_name = 'blog/index.html'

    def get_queryset(self):
        return get_post_queryset().order_by('-pub_date')


class PostDetailView(DetailView):
    """Cтраница с информацией о конкретном посте."""

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        """Запрос к бд с фильрами.
        Если пользователь и автор профиля страницы совпадают, то пользователь
        может просматривать неопубликованные посты.
        """
        post_id = self.kwargs[self.pk_url_kwarg]
        post = get_object_or_404(Post, id=post_id)
        author = post.author == self.request.user
        return sql_filters(
            Post.objects.select_related(
                'category', 'location', 'author'
            ).filter(id=post_id),
            author
        ).annotate(comment_count=Count("comments"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related(
                'author')
        )
        return context


class CategoryPostsView(ListView):
    """Cтраница с постами по категории."""

    paginate_by = NUMBER_OF_POSTS_PER_PAGE
    model = Post
    template_name = 'blog/category.html'

    def get_queryset(self):
        return get_post_queryset().filter(
            category__slug=self.kwargs['category_slug']
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = get_object_or_404(
            Category.objects.all(),
            slug=self.kwargs['category_slug'],
            is_published=True
        )

        context['category'] = category
        return context


class ProfileView(ListView):
    """Страница профиля пользователя."""

    paginate_by = NUMBER_OF_POSTS_PER_PAGE
    model = Post
    template_name = 'blog/profile.html'

    def get_queryset(self):
        author = False
        if str(self.kwargs['username']) == str(self.request.user):
            author = True
        qs = Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(author__username=self.kwargs['username'])
        return sql_filters(qs, author).annotate(
            comment_count=Count("comments")).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(
            User.objects.all(), username=self.kwargs['username'])
        context['profile'] = profile
        return context


class EditProfilView(UserPassesTestMixin, UpdateView):
    """Страница редактирования профиля."""

    model = User
    template_name = 'blog/user.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def test_func(self):
        """Проверка пользователя."""
        object = self.get_object()
        return str(object.username) == str(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        """Перенаправление пользователя не прошедшего проверку."""
        user_test_result = self.get_test_func()()

        if not user_test_result:
            return redirect('blog:profile',
                            username=self.get_object().username)
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Страница создания поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """Заполнение автора в форме."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class AuthorRedirectMixin:
    """Миксин для перенаправления неавтора на detail-представление поста."""

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not self.request.user.is_authenticated or not user_test_result:
            return redirect(
                reverse('blog:post_detail',
                        kwargs={'post_id': self.kwargs['post_id']})
            )
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(AuthorRedirectMixin, OnlyAuthorMixin, UpdateView):
    """Страница редактирования поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """Страница удаления поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')
