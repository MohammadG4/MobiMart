from rest_framework import serializers
from .models import Cart, CartItem, Coupon
from productsapp.models import Product

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["id", "code", "discount_percent", "active"]

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    product_price = serializers.ReadOnlyField(source="product.price")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "total_price",
            "added_at",
        ]

    def get_total_price(self, obj):
        return obj.total_price()
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "coupon",
            "items",
            "total_price",
            "discounted_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user"]  # user comes from request.user

    def get_total_price(self, obj):
        return obj.total_price()

    def get_discounted_price(self, obj):
        return obj.discounted_price()


