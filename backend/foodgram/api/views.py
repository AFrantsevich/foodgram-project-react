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
            return queryset
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


class SubscriptionsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        if self.request.user.id == int(self.kwargs.get("id")):
            raise serializers.ValidationError(
                {"error": "Нельзя подписаться на самого себя"})
        serializer.save(user=self.request.user,
                        author=get_object_or_404(
                            User, pk=self.kwargs.get("id")))

    @action(methods=['delete'], detail=False,)
    def delete(self, *args, **kwargs):
        obj = Subscribe.objects.filter(user=self.request.user).filter(
            author_id=self.kwargs.get("id"))
        if obj:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise serializers.ValidationError(
            {"error": "Подписки не существует"})


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.GET.get('search'):
            return Ingredient.objects.filter(
                name__iregex=self.request.GET.get('search'))
        return Ingredient.objects.all()


class FavoriteAndCartMixin(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    permission_classes = (IsAuthenticated | IsAdminUser, )

    def delete_obj(self, model, *args, **kwargs):
        obj = model.objects.filter(user=self.request.user).filter(
                recipe_id=self.kwargs.get("id"))
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise serializers.ValidationError(
            {"error": "Объекта удаления не существует"})

    def create_obj(self, model, serializer):
        if model.objects.filter(user=self.request.user).filter(
                recipe_id=self.kwargs.get("id")).exists():
            raise serializers.ValidationError(
                {"error": "Этот объект удже существуют в БД."})
        serializer.save(user=self.request.user,
                        recipe=get_object_or_404(
                            Recipe, pk=self.kwargs.get("id")))


class FavoriteViewSet(FavoriteAndCartMixin):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    @action(methods=['delete'], detail=False,)
    def delete(self, *args, **kwargs):
        return self.delete_obj(Favorite)

    def perform_create(self, serializer):
        return self.create_obj(Favorite, serializer)


class CartViewSet(FavoriteAndCartMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(methods=['delete'], detail=False,)
    def delete(self, *args, **kwargs):
        return self.delete_obj(Cart)

    def perform_create(self, serializer):
        return self.create_obj(Cart, serializer)


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
