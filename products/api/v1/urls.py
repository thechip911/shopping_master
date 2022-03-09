# python imports

# django imports

# third party imports
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
from .views import ProductModelViewSet, ProductSizeModelViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register("product", ProductModelViewSet, basename="product")  # Product CRUD
# router.register("product-size", ProductSizeModelViewSet, basename="product_size")  # Product CRUD

urlpatterns = [
    path("upload/", UploadBondsData.as_view(), name="upload-csv"),
]

urlpatterns += router.urls

# Add Multiple Format Support
urlpatterns = format_suffix_patterns(urlpatterns)
