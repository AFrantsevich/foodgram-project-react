from rest_framework import routers


from api.views import (TagsViewSet, RecipeViewSet,
                       SubscriptionsViewSet, IngredientsViewSet,
                       FavoriteViewSet, CartViewSet)


v1_router = routers.DefaultRouter()
v1_router.register(r'tags', TagsViewSet)
v1_router.register(r'recipes', RecipeViewSet)
v1_router.register(r'users/subscriptions', SubscriptionsViewSet)
v1_router.register(r'users/(?P<id>\d+)/subscribe', SubscriptionsViewSet)
v1_router.register(r'recipes/(?P<id>\d+)/favorite', FavoriteViewSet)
v1_router.register(r'recipes/(?P<id>\d+)/shopping_cart', CartViewSet)
v1_router.register(r'ingredients', IngredientsViewSet)
