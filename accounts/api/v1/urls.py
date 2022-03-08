# python imports

# django imports

# third party imports
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
# local imports
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.v1.views import ResetPassword, UserViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register("user", UserViewSet, basename="user")  # User Signup and Login

urlpatterns = [
    path("token", TokenObtainPairView.as_view(), name="token-obtain-pair"),  # Generate Token
    path(
        "generate-reset-password", ResetPassword.as_view(), name="generate-reset-password"
    ),  # Generate Reset Password Token
]

urlpatterns += router.urls

# Add Multiple Format Support
urlpatterns = format_suffix_patterns(urlpatterns)
