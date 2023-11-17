import webcolors

from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Ingredient,
                            Recipe,
                            Tag,
                            Favourite,
                            Shopping,
                            RecipeIngredient)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscribe, User


class UploadedBase64ImageSerializer(serializers.Serializer):
    file = Base64ImageField(required=True)
    created = serializers.DateTimeField()


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


class RecipeIngredientSafeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id',
                  'name',
                  'measurement_unit',
                  'amount')


class RecipeIngredientNotSafeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


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


class RecipeSafeSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSafeSerializer(many=True)
    is_favourited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'tag',
            'time',
            'ingredients',
            'description',
            'is_favorited',
            'is_in_shopping_cart',
            'image',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user.is_authenticated
        return Favourite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user.is_authenticated
        return Shopping.objects.filter(user=user, recipe=obj).exists()


class RecipeNotSafeSerializer(serializers.ModelSerializer):
    tag = serializers.PrimaryKeyRelatedField(many=True,
                                             queryset=Tag.objects.all())
    ingredients = RecipeIngredientNotSafeSerializer(many=True)
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'tag',
            'time',
            'ingredients',
            'description',
            'image'
        )

    def validation(self, obj):
        for field in ['name', 'description', 'time']:
            if not obj.get(field):
                raise serializers.ValidationError(
                    f'Поле {field} обязательно для заполнения'
                )
        if not obj.get('tag'):
            raise serializers.ValidationError(
                'Укажите минимум 1 тэг'
            )
        if not obj.get('ingredients'):
            raise serializers.ValidationError(
                'Укажите минимум 1 ингредиент'
            )
        ingredients_list = []
        for item in obj.get('ingredients'):
            ingredient = get_object_or_404(Ingredient, id=item['id'])
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты не могут повторяться'
                )
            if int(item['amount']) <= 0:
                raise serializers.ValidationError(
                    'Укажите количество ингредиента больше 0'
                )
            ingredients_list.append(ingredient)
        return obj

    @transaction.atomic
    def ingredients_set(self, recipe, ingredients):
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=ingredient['id']),
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    @transaction.atomic
    def create(self, validated_data):
        tag = validated_data.pop('tag')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        recipe.tag.set(tag)
        self.ingredients_set(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.time = validated_data.get(
            'time', instance.time
        )
        tag = validated_data.pop('tag')
        ingredients = validated_data.pop('ingredients')
        instance.tag.clear()
        instance.tags.set(tag)
        instance.ingredients.clear()
        self.ingredients_set(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSafeSerializer(instance,
                                    context=self.context).data


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

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
