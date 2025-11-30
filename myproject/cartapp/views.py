from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Cart, CartItem, Coupon
from .serializers import CartSerializer, CartItemSerializer, CouponSerializer
from productsapp.models import Product
from rest_framework.permissions import AllowAny,IsAdminUser, IsAuthenticated


# GET /cart/ → get cart

# POST /cart/add/ → add item

# POST /cart/update_qty/ → update qty

# POST /cart/remove/ → delete item

# POST /cart/apply-coupon/

# POST /cart/clear/



class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # Helper: get or create cart
    def get_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    # GET /cart/
    def list(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        # Validate product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist."}, status=404)

        # Stock check
        if product.stock < quantity:
            return Response(
                {"error": f"Only {product.stock} items left in stock."},
                status=400
            )

        cart = self.get_cart(request)

        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
        )

        # If exists, check stock for updated quantity
        if not created:
            if product.stock < cart_item.quantity + quantity:
                return Response(
                    {"error": f"Only {product.stock} items left in stock."},
                    status=400
                )
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response(CartSerializer(cart).data, status=200)

    @action(detail=False, methods=['post'])
    def update_qty(self, request):
        cart_item_id = request.data.get("cart_item_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=404)

        # Stock check
        if cart_item.product.stock < quantity:
            return Response(
                {"error": f"Only {cart_item.product.stock} left in stock."},
                status=400
            )

        cart_item.quantity = quantity
        cart_item.save()

        return Response(CartSerializer(cart_item.cart).data)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        cart_item_id = request.data.get("cart_item_id")

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=404)

        cart = cart_item.cart
        cart_item.delete()

        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'])
    def apply_coupon(self, request):
        code = request.data.get("code")
        cart = self.get_cart(request)

        try:
            coupon = Coupon.objects.get(code=code, active=True)
        except Coupon.DoesNotExist:
            return Response({"error": "Invalid or inactive coupon."}, status=404)

        cart.coupon = coupon
        cart.save()

        return Response(CartSerializer(cart).data)


    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = self.get_cart(request)
        cart.items.all().delete()
        cart.coupon = None
        cart.save()

        return Response(CartSerializer(cart).data)

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]
