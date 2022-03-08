from django.core.exceptions import ValidationError


class PasswordValidators:
    def password_validation(self, validated_data):
        password = validated_data["password"]
        confirm_password = validated_data.pop("confirm_password")
        if password != confirm_password:
            raise ValidationError({"password": "Password dont match"})
        return validated_data


def file_size_validator(value):  # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 5 MiB.")
