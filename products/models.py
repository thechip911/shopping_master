from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from accounts.models import CreatedUpdatedSoftDeleteMixin


class ProductSize(CreatedUpdatedSoftDeleteMixin):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.symbol} | {self.name}"

    class Meta:
        verbose_name = "Product Size"
        verbose_name_plural = "Product Sizes"
        ordering = ['-id']


class Product(CreatedUpdatedSoftDeleteMixin):
    class ProductFabric(models.IntegerChoices):
        nylon = 1, _("Nylon")
        cotton = 2, _("Cotton")
        polyester = 3, _("Polyester")

    class ProductColor(models.IntegerChoices):
        blue = 1, _("Blue")
        black = 2, _("Black")
        green = 3, _("Green")
        white = 4, _("White")

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_fabric = models.PositiveSmallIntegerField(choices=ProductFabric.choices)
    color = models.PositiveSmallIntegerField(choices=ProductColor.choices)
    size = models.ManyToManyField(ProductSize, related_name="products")
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product"
        ordering = ['-id']
