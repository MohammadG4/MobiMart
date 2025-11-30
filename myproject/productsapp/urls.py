from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
urlpatterns = []


router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'brands', views.BrandViewSet, basename='brand')
urlpatterns = router.urls