from rest_framework.routers import DefaultRouter
from .views import CartViewSet,CouponViewSet

router = DefaultRouter()
router.register("cart", CartViewSet, basename="cart")
router.register("coupon", CouponViewSet, basename="coupon")

urlpatterns = router.urls
