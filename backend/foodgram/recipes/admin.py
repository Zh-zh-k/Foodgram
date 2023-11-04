from django.contrib import admin

from .models import (Favourite, Ingredient, Recipe, RecipeIngredient,
                     RecipeTag, Shopping, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'measurement_unit')


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'color')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'time', 'description')
    search_fields = ('name', 'description')
    list_filter = ('pub_date',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favourite)
admin.site.register(Shopping)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
