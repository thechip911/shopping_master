# python imports

# django imports
from django.urls import include, path

# third-party imports

# inter-app imports

# local imports


urlpatterns = [
    path("v1/", include("accounts.api.v1.urls")),
]
