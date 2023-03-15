from rest_framework import serializers


from rest_framework.fields import SerializerMethodField


from foodgram.models import (Tags, Recipe,
                             Ingredient, RecipeTable,
                             Favorite, Cart, Subscribe)
from users.serializers import CustomUserSerializer
from .scripts import Base64ImageField


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tags


class RecipeTableSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="ingredient.id",
        queryset=Ingredient.objects.all()
    )
    name = serializers.CharField(source="ingredient.name", read_only=True)
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", read_only=True)

    class Meta:
        fields = ('id', 'amount', 'name', 'measurement_unit')
        model = RecipeTable


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeTableSerializer(many=True,
                                        source="recipetable_set", )
    image = Base64ImageField(required=True, allow_null=True)
    author = CustomUserSerializer(required=False)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'ingredients',
                  'tags', 'image',
                  'name', 'text',
                  'cooking_time', 'author',
                  'is_favorited', 'is_in_shopping_cart')
        model = Recipe

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return True if Favorite.objects.filter(recipe=obj).filter(
            user=self.context['request'].user) else False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return True if (Cart.objects.filter(recipe=obj)) else False

    def create(self, validated_data):
        ingredients = validated_data.pop('recipetable_set')
        tags = validated_data.pop('tags')
        recipe_obj = Recipe.objects.create(
            **validated_data, author=self.context['request'].user)
        recipe_obj.tags.set(tags)
        for ingredient in ingredients:
            RecipeTable.objects.create(
                ingredient=ingredient.get('ingredient').get('id'),
                recipe=recipe_obj,
                amount=ingredient.get("amount"))
        return recipe_obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.name)
        instance.image = validated_data.get('image', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.name)
        RecipeTable.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('recipetable_set')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        for ingredient in ingredients:
            RecipeTable.objects.create(
                ingredient=ingredient.get('ingredient').get('id'),
                recipe=instance,
                amount=ingredient.get("amount"))
        instance.save()
        return instance


class RecipeListSerializer(RecipeCreateSerializer):
    tags = TagsSerializer(many=True, read_only=True)


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    email = serializers.ReadOnlyField(source="author.email")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    recipes = serializers.SerializerMethodField()
    is_subscribed = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        fields = ("id",
                  "username",
                  "email",
                  "first_name",
                  "last_name",
                  'recipes',
                  'is_subscribed',
                  'recipes_count'
                  )
        model = Subscribe

    def get_recipes(self, obj):
        recipes_limit = self.context["request"].query_params.get(
            "recipes_limit")
        mylist = []
        model = Recipe.objects.filter(author=obj.author)
        for i in model:
            model_sr = RecipeSerializer(i)
            mylist.append(model_sr.data)
        return mylist[:int(recipes_limit):]

    def get_is_subscribed(self, contant_maker):
        return any(contant_maker.author == my_contantmakers.author
                   for my_contantmakers
                   in Subscribe.objects.filter(user=self.
                                               context["request"].user))

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredient


class FavoriteCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="recipe.id")
    name = serializers.ReadOnlyField(source="recipe.name")
    image = SerializerMethodField()
    cooking_time = serializers.ReadOnlyField(source="recipe.cooking_time")

    def get_image(self, obj):
        return str(Recipe.objects.get(id=obj.recipe_id).image)


class FavoriteSerializer(FavoriteCartSerializer):

    class Meta:
        fields = ('id', 'name', 'cooking_time', 'image')
        model = Favorite


class CartSerializer(FavoriteCartSerializer):

    class Meta:
        fields = ('id', 'name', 'cooking_time', 'image')
        model = Cart
