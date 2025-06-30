from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма для создания поста"""

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author', )
        widgets = {
            'pub_date': forms.TextInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    """Форма для создания комментария"""

    class Meta:
        model = Comment
        fields = ('text',)
