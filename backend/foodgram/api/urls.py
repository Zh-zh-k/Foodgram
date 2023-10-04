from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls), name='api-root'),
]
