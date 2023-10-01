from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tag', 'time', 'ingredients', 'description', 'image')
        labels = {
            'name': 'Название',
            'tag': 'Тэги',
            'time': 'Время приготовления',
            'ingredients': 'Необходимые ингредиенты',
            'description': 'Текст рецепта',
            'image': 'Фото блюда',
        }
        help_text = {
            'name': 'Укажите название рецепта',
            'tag': 'Установите тэги',
            'time': 'Укажите время приготовления в минутах',
            'ingredients': 'Перечислите необходимые ингредиенты',
            'description': 'Напишите свой рецепт',
            'image': 'Добавьте фото готового блюда',
        }
