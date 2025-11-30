from django.db import models
from django.conf import settings
from decimal import Decimal


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Cart of {self.user.email}"
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    def discounted_price(self):
      total = self.total_price()
    
      if self.coupon and self.coupon.active:
          discount_percentage = Decimal(self.coupon.discount_percent) / Decimal(100)
          discount = discount_percentage * total
          return total - discount
      
      return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("productsapp.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.email}'s cart"

    def total_price(self):
        return self.quantity * self.product.price
    
    


