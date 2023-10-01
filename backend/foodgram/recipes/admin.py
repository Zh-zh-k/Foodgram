from django.contrib import admin

from .models import Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'time', 'ingredients', 'description')
    search_fields = ('name', 'description')
    list_filter = ('pub_date',)


admin.site.register(Recipe, RecipeAdmin)

admin.site.register(Tag)
