from rest_framework import serializers
from .models import Order, OrderItem
from productsapp.models import Product  # import Product model


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]  # include any fields you want


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # nested serializer

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]
        read_only_fields = ["product", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    coupon = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "total_price",
            "final_price",
            "coupon",
            "items",
            "created_at",
            "shipping_address",
        ]
        read_only_fields = [
            "user",
            "status",
            "total_price",
            "final_price",
            "coupon",
            "items",
            "created_at",
        ]
