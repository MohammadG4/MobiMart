import meilisearch
from django.conf import settings
from productsapp.models import ProductImage

client = meilisearch.Client(
    settings.MEILISEARCH_URL,
    settings.MEILISEARCH_API_KEY
)

def get_product_index():
    return client.index(settings.MEILISEARCH_INDEX)

def setup_index():
    index = get_product_index()
    index.update_settings({
        "searchableAttributes": ["name", "description"],
        "filterableAttributes": ["category", "price", "brand"],
        "sortableAttributes": ["price", "created_at"]
    })

def index_product(product):
    index = get_product_index()
    
    # image_url = ProductImage.objects.filter(product=product, is_main=True).first().image.url
    main_image = product.images.filter(is_main=True).first()
    if not main_image:
        main_image = product.images.first()
    image_url = main_image.image.url if main_image else None
    doc = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "brand": product.brand.name if product.brand else None,
        "price": float(product.price),
        "category": product.category.name if product.category else None,
        "created_at": product.created_at.isoformat(),
        "image_url": image_url,
    }
    index.add_documents([doc])


def delete_product(product_id):
    index = get_product_index()
    index.delete_document(product_id)
