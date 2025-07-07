"""Структура базы данных.
В python классах (моделях) описываются типы полей и связи между таблицами.
Модель User встроена в Django и просто импортируется.
"""


from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()

TITLE_MAX_LENGTH = 256
NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50
TEXT_PREVIEW_LENGTH = 50


class BaseModel(models.Model):
    """Абстрактная модель.
    1) is_published - используется для выбора (публиковать или нет) запись из
    бд, обязательное поле, содержит булево значение. default - значение по
    умолчанию; help_text - подсказка, рядом с полем; verbose_name -
    человекочитаемое название. 2) created_at - отображает время создания
    записи, обязательное поле, содержит дату и время. Параметр auto_now_add -
    автоматически создает метку при создании строки в базе данных.
    """

    is_published = models.BooleanField(
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        verbose_name='Опубликовано'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:

        abstract = True


class Category(BaseModel):
    """Модель с категориями.
    Наследуется от абстрактной модели BaseModel (получает все ее атрибуты).
    1) title - отображает название категории, обязательное поле, содержит
    строку; 2) description - отображает описание категории, обязательное поле,
    содержит текст; 3) slug - идентификатор страницы для URL, обязательное
    поле, содержит символы латиницы, цифры, дефис и подчёркивание, unique -
    уникальное поле.
    """

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
        help_text=('Идентификатор страницы для URL; разрешены символы латиницы'
                   ', цифры, дефис и подчёркивание.'),
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title[:TEXT_PREVIEW_LENGTH]


class Location(BaseModel):
    """Модель с локациями.
    name - отображает название места, обязательное поле, содержит строку.
    """

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_PREVIEW_LENGTH]


class Post(BaseModel):
    """Модель с постами.
    1) title - используется для отображения заголовка, обязательное поле,
    содержит строку; 2) text - отображает текст, обязательное поле, содержит
    текст; 3) pub_date - отображает дату публикации, обязательное поле,
    содержит дату и время; 4) author - внешний ключ(FK) к таблице с
    пользователями, обязательное поле, каскадное удаление связанных объектов;
    5) location - внешний ключ(FK) к таблице с локациями, необязательное поле
    (blank=True), устанавливается NULL при удалении связанных объектов;
    6) category - внешний ключ(FK) к таблице с категориями, обязательное поле,
    устанавливается NULL при удалении связанных объектов.
    """

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        help_text=('Если установить дату и время в будущем — можно делать '
                   'отложенные публикации.'),
        verbose_name='Дата и время публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title[:TEXT_PREVIEW_LENGTH]


class Comment(models.Model):
    """Модель комментария."""

    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TEXT_PREVIEW_LENGTH]
