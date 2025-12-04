from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('userapp.urls')),
    path('api/', include('productsapp.urls')),
    path('api/', include('cartapp.urls')),
    path('api/', include('orderapp.urls')),
    path('api/search/', include('searchapp.urls')),
    ]