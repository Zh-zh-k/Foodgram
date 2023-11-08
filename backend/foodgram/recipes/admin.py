from django.contrib import admin

from .models import (Favourite, Ingredient, Recipe, RecipeIngredient,
                     RecipeTag, Shopping, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'measurement_unit')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'color')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'time', 'description')
    search_fields = ('name', 'description')
    list_filter = ('pub_date',)


admin.site.register(Favourite)
admin.site.register(Shopping)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
