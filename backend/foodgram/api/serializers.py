import base64

import webcolors
from django.core.files.base import ContentFile
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscribe, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'title', 'slug', 'color')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'title', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'pub_date',
            'author',
            'tag',
            'time',
            'ingredients',
            'description',
            'image'
        )


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(slug_field='username',
                                          queryset=User.objects.all(),)

    def validate_subscription(self, author):
        if author == self.context['request'].user:
            raise serializers.ValidationError('Нельзя подписаться на самого'
                                              'себя')
        return author

    class Meta:
        fields = ('id', 'user', 'author')
        model = Subscribe
        validators = [UniqueTogetherValidator(queryset=Subscribe.objects.all(),
                                              fields=['user', 'author'])]
