from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()

TAG_CHOICES = (
    ('Breakfast', 'Завтрак'),
    ('Lunch', 'Обед'),
    ('Dinner', 'Ужин'),
)


class Tag(models.Model):
    title = models.CharField(max_length=15, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message="Введите значение цвета в HEX-формате"
            )
        ]
    )

    class Meta:
        ordering = ['title',]
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.TextField()
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        ordering = ['title',]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.measurement_unit}'


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
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
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


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fav_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='fav_recipe'
    )

    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_user_fav_recipe')
        ]


class Shopping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shop_recipe'
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_user_shop_recipe')
        ]


class RecipeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'
