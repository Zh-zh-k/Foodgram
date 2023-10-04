from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import RecipeViewSet, TagViewSet, SubscribeViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('subscribtions', SubscribeViewSet, basename='subscriptions')

urlpatterns = [
    path('', include(router.urls), name='api-root'),
]
