from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response

from recipes.models import RecipeIngredient, Shopping, User


def get_shopping_list(user: User):
    if not Shopping.objects.filter(user=user).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    ingredients = RecipeIngredient.objects.filter(
        recipe__shopping_cart__user=user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(
        total_amount=Sum('amount')
    ).values_list(
        'total_amount',
        'ingredient__name',
        'ingredient__measurement_unit'
    )
    file_content = []
    for ingredient in ingredients:
        file_content += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
        ])
    return file_content
