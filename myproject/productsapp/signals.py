from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from .search_index import index_product, delete_product

@receiver(post_save, sender=Product)
def product_saved(sender, instance, **kwargs):
    index_product(instance)

@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    delete_product(instance.id)
