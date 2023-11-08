from django_filters import FilterSet
from django_filters.rest_framework import filters

from recipes.models import Recipe, Tag


class RecipeCustomFilter(FilterSet):
    tags = filters.MultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenicated:
            return queryset.filter(fav_recipe__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenicated:
            return queryset.filter(shop_cart__user=self.request.user)
        return queryset
