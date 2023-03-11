from django.db import models
from foodgram.validators import validate_slug
from users.models import User
from rest_framework.validators import UniqueValidator


class Tags(models.Model):
    name = models.CharField('Название',
                            max_length=256,
                            unique=True)
    color = models.CharField('Цвет',
                             max_length=16,
                             unique=True)
    slug = models.SlugField('Слаг', unique=True,
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
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        to="Recipe",
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField('Количество', max_digits=5, decimal_places=2)


class Ingredient(models.Model):
    name = models.CharField('Имя', max_length=200)
    measurement_unit = models.CharField('Ед.измерения', max_length=200)

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
    name = models.CharField('Название',
                            max_length=200)
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         through='RecipeTable',)
    image = models.ImageField(upload_to='static/image/')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    tags = models.ManyToManyField(
        Tags,
        related_name='recipes')
    cooking_time = models.IntegerField('Время приготовления')

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe'
            ),
        ]


class Subscribe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='subscribes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='subscribe_recipe'
            ),
        ]


class FavoriteCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='%(class)s',
                             null=True)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='%(class)s',
                               null=True)

    class Meta:
        abstract = True


class Cart(FavoriteCart):
    pass


class Favorite(FavoriteCart):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            ),
        ]
