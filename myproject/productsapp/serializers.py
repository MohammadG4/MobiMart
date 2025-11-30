from rest_framework import serializers
from .models import Product, ProductImage, MobileSpecs,Brand, Category


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main']


class MobileSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileSpecs
        fields = [
            'ram', 'storage', 'cpu', 'gpu',
            'camera_main', 'camera_front',
            'battery', 'screen_size', 'screen_type',
            'os', 'sim'
        ]


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(
        queryset=Brand.objects.all(),
        slug_field='name'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )

    specs = MobileSpecsSerializer()

    # Write-only: used when creating
    images = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )

    # Read-only: returned in GET requests
    images_data = ProductImageSerializer(source="images", many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'category',
            'price', 'stock', 'description', 'created_at',
            'specs', 'images', 'images_data'
        ]

    def create(self, validated_data):
        specs_data = validated_data.pop('specs')
        images_data = validated_data.pop('images')

        product = Product.objects.create(**validated_data)

        MobileSpecs.objects.create(product=product, **specs_data)

        for img in images_data:
            ProductImage.objects.create(
                product=product,
                image=img["image"],        # FILE
                is_main=img.get("is_main", False)
            )

        return product
    
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

