from django.db import transaction
from rest_framework import permissions

from accounts.fields import UserSignupFields
from core_libs.validators import PasswordValidators


class UserModelSerializer(UserSignupFields, PasswordValidators):
    def __init__(self, *args, **kwargs) -> None:
        request = kwargs.get("context")["request"]
        self.FIELD_NAMES = UserSignupFields.SIGNUP_FIELDS
        if request.method in permissions.SAFE_METHODS:
            self.FIELD_NAMES = UserSignupFields.BASE_FIELDS
        if request.method == "PATCH":
            self.FIELD_NAMES = UserSignupFields.PASSWORD_FIELDS
        self.meta_obj.model = self.MODEL_CLASS
        self.meta_obj.fields = self.FIELD_NAMES
        self.meta_obj.extra_kwargs = self.EXTRA_KWARGS
        super().__init__(*args, **kwargs)

    def to_representation(self, instance) -> str:
        data = super(UserModelSerializer, self).to_representation(instance)
        data["profile_picture"] = instance.get_profile_picture
        return data

    def validate(self, validated_data):
        validated_data = self.password_validation(validated_data)
        return validated_data

    @transaction.atomic
    def create(self, validated_data):
        instance = super(UserModelSerializer, self).create(validated_data)
        self.create_update_password(instance, validated_data)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super(UserModelSerializer, self).update(instance, validated_data)
        self.create_update_password(instance, validated_data)
        return instance


class ProfileUpdateModelSerializer(UserSignupFields, PasswordValidators):
    def __init__(self, *args, **kwargs) -> None:
        request = kwargs.get("context")["request"]
        self.FIELD_NAMES = UserSignupFields.BASE_FIELDS
        self.meta_obj.model = self.MODEL_CLASS
        self.meta_obj.fields = self.FIELD_NAMES
        self.meta_obj.extra_kwargs = self.EXTRA_KWARGS
        super().__init__(*args, **kwargs)

    def to_representation(self, instance) -> str:
        data = super(ProfileUpdateModelSerializer, self).to_representation(instance)
        data["profile_picture"] = instance.get_profile_picture
        return data
