from django.contrib import admin

# Register your models here.
from .models import Brand, Category, Product, ProductImage, MobileSpecs
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(MobileSpecs)
