from django.contrib import admin
from .models import Ingredient, Recipe, Favorite, User


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'Favorite_count')
    search_fields = ('name', 'author__username', 'tags__name', )

    def Favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('username', 'email')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')


admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
