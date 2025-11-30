from django.db import models
from cloudinary.models import CloudinaryField

class Brand(models.Model):
    BRAND_CHOICES = [
        ('apple', 'Apple'),
        ('samsung', 'Samsung'),
        ('xiaomi', 'Xiaomi'),
        ('oppo', 'Oppo'),
        ('vivo', 'Vivo'),
        ('realme', 'Realme'),
        ('huawei', 'Huawei'),
        ('honor', 'Honor'),
        ('infinix', 'Infinix'),
        ('tecno', 'Tecno'),
        ('oneplus', 'OnePlus'),
        ('google', 'Google Pixel'),
        ('motorola', 'Motorola'),
        ('nokia', 'Nokia'),
        ('sony', 'Sony'),
        ('asus', 'ASUS'),
        ('lenovo', 'Lenovo'),
        ('zte', 'ZTE'),
        ('meizu', 'Meizu'),
        ('sharp', 'Sharp'),
        ('htc', 'HTC'),
        ('lg', 'LG'),
        ('blackberry', 'BlackBerry'),
        ('nothing', 'Nothing'),
        ('redmagic', 'RedMagic (ZTE Nubia)'),
        ('rog', 'ASUS ROG Phone'),
        ('poco', 'POCO'),
        ('iqoo', 'iQOO'),
    ]

    name = models.CharField(max_length=100, choices=BRAND_CHOICES)

    def __str__(self):
        return self.name


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('flagship', 'Flagship'),
        ('midrange', 'Midrange'),
        ('budget', 'Budget'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = CloudinaryField('image', folder=lambda instance: f"products/{instance.product.id}")
    is_main = models.BooleanField(default=False)
    def __str__(self):
        return f"Image for {self.product.name}"

class MobileSpecs(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="specs"
    )

    ram = models.CharField(max_length=20)
    storage = models.CharField(max_length=20)
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100, blank=True, null=True)

    camera_main = models.CharField(max_length=255)
    camera_front = models.CharField(max_length=255)

    battery = models.CharField(max_length=50)
    screen_size = models.CharField(max_length=50)
    screen_type = models.CharField(max_length=50)

    os = models.CharField(max_length=50)
    sim = models.CharField(max_length=50)

    def __str__(self):
        return f"Specs for {self.product.name}"
