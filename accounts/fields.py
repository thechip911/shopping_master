"""
Base Fields for serializers.py
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from core_libs.serializers import BaseModelSerializer

User = get_user_model()


class BaseUserFields(BaseModelSerializer):
    """
    Serializer fields for User
    """

    MODEL_CLASS = User
    BASE_FIELDS = (
        "id",
        "name",
        "first_name",
        "last_name",
        "mobile_number",
        "email",
        "profile_picture",
    )


class UserPasswordFields(BaseModelSerializer):
    """
    Fields for Password
    """

    confirm_password = serializers.CharField(write_only=True, required=False)

    EXTRA_KWARGS = {
        "password": {"write_only": True},
        "confirm_password": {"write_only": True},
    }

    PASSWORD_FIELDS = (
        "password",
        "confirm_password",
    )


class UserSignupFields(BaseUserFields, UserPasswordFields):
    """
    Fields for SignUp
    """

    SIGNUP_FIELDS = BaseUserFields.BASE_FIELDS + UserPasswordFields.PASSWORD_FIELDS

    def create_update_password(self, instance, validated_data) -> None:  # pylint: disable=no-self-use
        """
        Function for Creating/Updating the Password
        """
        password = validated_data["password"]
        instance.set_password(password)
        instance.save()
