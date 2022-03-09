# python imports

# django imports
from django.urls import include, path

# third-party imports

# inter-app imports

# local imports

# app name
app_name = "products"

urlpatterns = [
    path("api/", include("products.api.urls")),  # apis
]
