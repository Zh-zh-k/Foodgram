from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import format_html

User = get_user_model()

TAG_CHOICES = (
    ("Breakfast", "Завтрак"),
    ("Lunch", "Обед"),
    ("Dinner", "Ужин"),
)


class Tag(models.Model):
    title = models.CharField(max_length=15,
                             choices=TAG_CHOICES)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7,
                             default="#ffffff",
                             unique=True)

    def __str__(self):

        return self.title

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.color,
        )


class Recipe(models.Model):
    name = models.TextField(
        verbose_name='Название рецепта'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг'
    )
    time = models.DurationField(
        verbose_name='Время приготовления'
    )
    ingredients = models.TextField(
        verbose_name='Ингредиенты'
    )
    description = models.TextField(
        verbose_name='Описание рецепта'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follower_following')
        ]
