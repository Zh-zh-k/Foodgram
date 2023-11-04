from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (Recipe,
                            Tag,
                            Ingredient,
                            Favourite,
                            Shopping,
                            RecipeIngredient)
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer
from .permissions import AuthorOrReadOnly, ReadOnly, AdminOnly
from .filters import RecipeCustomFilter


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOnly,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeCustomFilter

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated,]
            )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            serializer = RecipeSerializer(recipe, data=request.data)
            serializer.is_valid(raise_exception=True)
            if Favourite.objects.filter(user=request.user,
                                        recipe=recipe).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Favourite.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Favourite, user=request.user,
                              recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated,]
            )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            serializer = RecipeSerializer(recipe, data=request.data)
            serializer.is_valid(raise_exception=True)
            if Shopping.objects.filter(user=request.user,
                                       recipe=recipe).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Shopping.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Shopping, user=request.user,
                              recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        if Shopping.objects.filter(user=user).exists():
            ingredients = RecipeIngredient.objects.filter(
                recipe__shopping_cart__user=request.user
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
            file = f'{user.username}_shopping_list.txt'
            response = HttpResponse(file_content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename={file}'
            return response
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
