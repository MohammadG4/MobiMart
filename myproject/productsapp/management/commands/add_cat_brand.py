from django.core.management.base import BaseCommand
from productsapp.models import Brand, Category

class Command(BaseCommand):
    help = "Populate Brand and Category tables with choices"

    def handle(self, *args, **kwargs):
        for key, name in Brand.BRAND_CHOICES:
            Brand.objects.get_or_create(name=name)
        for key, name in Category.CATEGORY_CHOICES:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("✅ Brands and Categories populated successfully!"))
