from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

TAG_CHOICES = (
    ('Breakfast', 'Завтрак'),
    ('Lunch', 'Обед'),
    ('Dinner', 'Ужин'),
)


class Tag(models.Model):
    title = models.CharField(max_length=15)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7,
                             unique=True)

    def __str__(self):

        return self.title


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
        through='RecipeTag',
        choices=TAG_CHOICES
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
        upload_to='recipes/images/',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Subscribe(models.Model):
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


class RecipeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'
