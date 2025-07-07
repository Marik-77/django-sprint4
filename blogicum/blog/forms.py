from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма для создания поста"""

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author', )
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].input_formats = ['%Y-%m-%dT%H:%M']


class CommentForm(forms.ModelForm):
    """Форма для создания комментария"""

    class Meta:
        model = Comment
        fields = ('text',)
