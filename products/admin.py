from django.contrib import admin

from core_libs.admin_fields import BaseAdminReadOnlyFields
from products.models import Product, ProductSize


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ("id", 'name',"symbol")
    list_filter = ('symbol', )


@admin.register(Product)
class Product(BaseAdminReadOnlyFields):
    list_display = ("id", "name", "price", "discount_price", "product_fabric", "color", "is_active")
    search_fields = (
        "name",
        "color",
    )
    list_filter = (
        "is_active",
        "product_fabric",
        "color",
        "size"
    )
