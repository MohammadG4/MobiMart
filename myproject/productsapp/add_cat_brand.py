from products.models import Brand, Category

# --- Populate Brands ---
for key, name in Brand.BRAND_CHOICES:
    Brand.objects.get_or_create(name=name)

# --- Populate Categories ---
for key, name in Category.CATEGORY_CHOICES:
    Category.objects.get_or_create(name=name)

print("✅ Brands and Categories populated successfully!")
