"""Дополнительные миксины."""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse

from blog.models import Comment


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин проверки авторства."""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class CommentMixin:
    """Миксин для изменения и удаления комментрария."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )
