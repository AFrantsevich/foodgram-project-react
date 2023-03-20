from django.db import models
from api.validators import validate_slug
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator


class Tags(models.Model):
    name = models.CharField(verbose_name='name',
                            max_length=256,
                            unique=True)
    color = models.CharField(verbose_name='color',
                             max_length=16,
                             unique=True)
    slug = models.SlugField(verbose_name='slug', unique=True,
                            max_length=200,
                            validators=(validate_slug,
                                        UniqueValidator)
                            )

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color', 'slug'],
                name='unique_tags'
            ),
        ]


class RecipeTable(models.Model):
    ingredient = models.ForeignKey(
        "Ingredient",
        verbose_name='ingredient',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        "Recipe",
        verbose_name='recipe',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(verbose_name='amount',
                                 max_digits=5,
                                 decimal_places=2)

    def __str__(self):
        return 'RecipeTable'


class Ingredient(models.Model):
    name = models.CharField(verbose_name='ingredient',
                            max_length=200)
    measurement_unit = models.CharField(verbose_name='measurement_unit',
                                        max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            ),
        ]


class Recipe(models.Model):
    name = models.CharField(verbose_name='name',
                            max_length=200)
    text = models.TextField(verbose_name='description')
    ingredients = models.ManyToManyField(Ingredient, verbose_name='ingredient',
                                         related_name='recipes',
                                         through='RecipeTable',)
    image = models.ImageField(verbose_name='image',
                              upload_to='media/static/image/')
    author = models.ForeignKey(get_user_model(),
                               verbose_name='author',
                               on_delete=models.CASCADE,
                               related_name='recipes')
    tags = models.ManyToManyField(
        Tags,
        verbose_name='tag',
        related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='cooking_time')

    def __str__(self):
        return 'Рецепты'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe'
            ),
        ]


class Subscribe(models.Model):
    user = models.ForeignKey(get_user_model(),
                             verbose_name='subscribe',
                             on_delete=models.CASCADE, )
    author = models.ForeignKey(get_user_model(),
                               verbose_name='author',
                               on_delete=models.CASCADE,
                               related_name='subscribes')

    def __str__(self):
        return 'Подписчики'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='subscribe_recipe'
            ),
        ]


class Cart(models.Model):
    user = models.ForeignKey(get_user_model(),
                             verbose_name='user',
                             on_delete=models.CASCADE,
                             related_name='carts',
                             null=True)
    recipe = models.ForeignKey(Recipe,
                               verbose_name='recipe',
                               on_delete=models.CASCADE,
                               related_name='carts',
                               null=True)

    def __str__(self):
        return 'Cart'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='cart_recipe'
            ),
        ]


class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(),
                             verbose_name='author',
                             on_delete=models.CASCADE,
                             related_name='favorites',
                             null=True)
    recipe = models.ForeignKey(Recipe,
                               verbose_name='recipe',
                               on_delete=models.CASCADE,
                               related_name='favorites',
                               null=True)

    def __str__(self):
        return 'Favorite'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_recipe'
            ),
        ]
