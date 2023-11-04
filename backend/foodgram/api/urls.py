from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import RecipeViewSet, TagViewSet, IngredientViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls), name='api-root'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
