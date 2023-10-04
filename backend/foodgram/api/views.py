from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipe, Tag, User
from .serializers import RecipeSerializer, TagSerializer, SubscribeSerializer
from .permissions import AuthorOrReadOnly, ReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tag',)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('=user__username', '=author__username')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
