from django.db import models
from django.conf import settings
from productsapp.models import Product
from cartapp.models import Coupon  # if you store coupons in a separate app

class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)          # price before discount
    final_price = models.DecimalField(max_digits=10, decimal_places=2)          # after discount
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot

    def __str__(self):
        return f"{self.product} x {self.quantity}"
