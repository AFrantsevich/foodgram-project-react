from django.contrib import admin
from .models import Ingredient, Recipe, Favorite, Tags
from users.models import User
from django.contrib.auth.admin import UserAdmin


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'Favorite_count')
    search_fields = ('name', 'author__username', 'tags__name', )

    def Favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'slug')


admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tags, TagsAdmin)
