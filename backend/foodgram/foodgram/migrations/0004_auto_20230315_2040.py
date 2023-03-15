# Generated by Django 3.2.18 on 2023-03-15 17:40

import api.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rest_framework.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foodgram', '0003_alter_recipe_image'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_favorite',
        ),
        migrations.AlterField(
            model_name='cart',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='foodgram.recipe', verbose_name='recipe'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='foodgram.recipe', verbose_name='recipe'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=200, verbose_name='measurement_unit'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, verbose_name='ingredient'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(verbose_name='cooking_time'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='static/image/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='foodgram.RecipeTable', to='foodgram.Ingredient', verbose_name='ingredient'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='foodgram.Tags', verbose_name='tag'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='recipetable',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='amount'),
        ),
        migrations.AlterField(
            model_name='recipetable',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.ingredient', verbose_name='ingredient'),
        ),
        migrations.AlterField(
            model_name='recipetable',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.recipe', verbose_name='recipe'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribes', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='subscribe'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='color',
            field=models.CharField(max_length=16, unique=True, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, validators=[api.validators.validate_slug, rest_framework.validators.UniqueValidator], verbose_name='slug'),
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='cart_recipe'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='favorite_recipe'),
        ),
    ]
