from rest_framework.serializers import ModelSerializer

from products.models import Product, ProductSize


class ProductSizeModelSerializer(ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ("id", "name", "symbol")


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "discount_price",
            "product_fabric",
            "color",
            "size",
            "description",
            "is_active",
        )
