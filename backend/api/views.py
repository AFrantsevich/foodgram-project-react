from rest_framework import generics
from rest_framework import viewsets, status, serializers


from django.http import HttpResponse
from django.shortcuts import get_object_or_404


from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, )


from .serializers import (TagsSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, SubscribeSerializer,
                          IngredientSerializer, FavoriteSerializer,
                          CartSerializer)
from foodgram.models import (Tags, Recipe,
                             Subscribe, Ingredient,
                             Favorite, Cart)
from .permission import IsAuthenticatedOrReadOnlyIsAuthorOrAdmin
from .resources import CartResource
from users.models import User


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    http_method_names = ['get']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnlyIsAuthorOrAdmin, )

    def get_serializer_class(self):
        if (self.request.method == 'POST'
                or self.request.method == 'PATCH'):
            return RecipeCreateSerializer
        elif self.request.method == 'GET':
            return RecipeListSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        if self.request.user.is_anonymous:
            is_favorited, is_in_shopping_cart = False, False
        is_favorited = self.request.query_params.get("is_favorited")
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart")
        author = self.request.query_params.get("author")
        tags = self.request.query_params.get("tags")
        if is_favorited == '1':
            queryset = Recipe.objects.filter(
                favorites__user=self.request.user)
        elif is_favorited == '0':
            queryset = Recipe.objects.exclude(
                favorites__user=self.request.user)
        elif is_in_shopping_cart == '1':
            queryset = Recipe.objects.filter(
                carts__user=self.request.user)
        elif is_in_shopping_cart == '0':
            queryset = Recipe.objects.exclude(
                carts__user=self.request.user)
        elif author:
            queryset = Recipe.objects.filter(
                author_id=author)
        elif tags:
            queryset = Recipe.objects.filter(
                tags__slug__iregex=tags)
        return queryset


class FavoriteCartSubscriptionMixin(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    permission_classes = (IsAuthenticated | IsAdminUser, )

    def get_query(self, model):
        return model.objects.filter(
            user=self.request.user)

    def delete_obj(self, model, model2, field, field2, *args, **kwargs):
        obj_mod = get_object_or_404(model2, pk=self.kwargs.get("id"))
        obj = model.objects.filter(**{field: self.request.user,
                                      field2: obj_mod})
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise serializers.ValidationError(
            {"error": "Объекта удаления не существует"})

    def create_obj(self, model, model2, serializer, field, field2, ):
        obj_mod = get_object_or_404(model2, pk=self.kwargs.get("id"))
        if model.objects.filter(**{field: self.request.user,
                                   field2: obj_mod}).exists():
            raise serializers.ValidationError(
                {"error": "Этот объект уже существует в БД."})
        serializer.save(**{field: self.request.user, field2: obj_mod})


class SubscriptionsViewSet(FavoriteCartSubscriptionMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return self.get_query(Subscribe)

    def perform_create(self, serializer):
        if self.request.user.id == int(self.kwargs.get("id")):
            raise serializers.ValidationError(
                {"error": "Нельзя подписаться на самого себя"})
        return self.create_obj(Subscribe, User, serializer,
                               field='user', field2='author')

    @action(methods=['delete'], detail=False,)
    def delete(self, *args, **kwargs):
        return self.delete_obj(Subscribe, User,
                               field='user', field2='author')


class FavoriteViewSet(FavoriteCartSubscriptionMixin):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return self.get_query(Favorite)

    @action(methods=['delete'], detail=False,)
    def delete(self, *args, **kwargs):
        return self.delete_obj(Favorite, Recipe, field='user',
                               field2='recipe')

    def perform_create(self, serializer):
        return self.create_obj(Favorite, Recipe, serializer,
                               field='user', field2='recipe', )


class CartViewSet(FavoriteCartSubscriptionMixin):
    serializer_class = CartSerializer

    def get_queryset(self):
        return self.get_query(Cart)

    @action(methods=['delete'], detail=False,)
    def delete(self, *args, **kwargs):
        return self.delete_obj(Cart, Recipe,
                               field='user', field2='recipe',)

    def perform_create(self, serializer):
        return self.create_obj(Cart, Recipe, serializer,
                               field='user', field2='recipe',)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.GET.get('name'):
            return Ingredient.objects.filter(
                name__iregex=self.request.GET.get('name'))
        return Ingredient.objects.all()


class DownlodShoppingCart(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()

    def list(self, request, *args, **kwargs):
        employee_resource = CartResource(user=request.user)
        dataset = employee_resource.export()
        response = HttpResponse(dataset.xls,
                                content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="exported_data.xls"')
        return response
