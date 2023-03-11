from django.contrib import admin
from django.urls import path, include
from api.urls import v1_router


from foodgram.views import DownlodShoppingCart


urlpatterns = [
    path('api/recipes/download_shopping_cart/', DownlodShoppingCart.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(v1_router.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
