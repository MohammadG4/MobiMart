from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


from .models import Order, OrderItem
from .serializers import OrderSerializer
from cartapp.models import Cart, CartItem


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'user__email', 'coupon__code']   # admin can filter by these
    search_fields = ['user__email', 'coupon__code']                # search by email or coupon code
    ordering_fields = ['created_at', 'total_price', 'final_price'] # order by these fields
    ordering = ['-created_at']   


    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()         # admin sees all orders
        return Order.objects.filter(user=self.request.user)   # user sees only his own

    def perform_create(self, serializer):
        pass  # not used

    # ---------------------------
    # USER CHECKOUT
    # ---------------------------
    @action(detail=False, methods=["post"])
    def checkout(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=400)

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        order = Order.objects.create(
            user=user,
            total_price=cart.total_price(),
            final_price=cart.discounted_price() or cart.total_price(),
            coupon=cart.coupon,
            shipping_address=request.data.get("shipping_address", "")
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()
        cart.total_price = 0
        cart.discounted_price = 0
        cart.coupon = None
        cart.save()

        return Response(OrderSerializer(order).data, status=201)

    # ---------------------------
    # USER CANCEL ORDER
    # ---------------------------
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status != "PENDING":
            return Response({"error": "Only pending orders can be cancelled"}, status=400)

        order.status = "CANCELLED"
        order.save()

        return Response({"message": "Order cancelled successfully"}, status=200)

    # ---------------------------
    # ADMIN CHANGE STATUS
    # ---------------------------
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=400)

        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data, status=200)
