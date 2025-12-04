from django.core.management.base import BaseCommand
from productsapp.models import Product
from productsapp.search_index import index_product, setup_index

class Command(BaseCommand):
    help = 'Re-index all products into Meilisearch'

    def handle(self, *args, **options):
        # Optional: initialize index settings
        self.stdout.write("Setting up Meilisearch index settings...")
        setup_index()

        products = Product.objects.all()
        total = products.count()
        self.stdout.write(f"Indexing {total} products...")

        for i, product in enumerate(products, start=1):
            index_product(product)
            if i % 50 == 0 or i == total:
                self.stdout.write(f"Indexed {i}/{total}")

        self.stdout.write(self.style.SUCCESS("All products have been indexed successfully."))
