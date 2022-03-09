import os
import urllib

import pyotp
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.templatetags.static import static
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomUserManager
from core_libs.utils import profile_picture_upload
from core_libs.validators import file_size_validator


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True, deleted_at=timezone.now())


class SoftDeleteAllManager(models.Manager):
    """
    Custom manager to access all records.
    """

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteDefaultManager(SoftDeleteAllManager):
    """
    By default we don't include soft-deleted records.
    """

    def get_queryset(self):
        return super(SoftDeleteDefaultManager, self).get_queryset().filter(is_deleted=False)


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(
        default=False,
        help_text=_(_("Mark an item deleted without actually deleting it from database. I.e, soft deletion.")),
    )
    deleted_at = models.DateTimeField(blank=True, null=True, help_text=_("Soft deletion date and time."))

    objects = SoftDeleteDefaultManager()
    all_objects = SoftDeleteAllManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class CreatedUpdatedSoftDeleteMixin(SoftDeleteMixin):
    created_by_id = models.IntegerField(help_text=_("User ID from the Authentication system"), null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The creation time, always in Asia/Kolkata timezone."),
    )

    updated_by_id = models.IntegerField(help_text=_("User ID from the Authentication system"), null=True)
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The last update time, always in Asia/Kolkata timezone."),
    )

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, CreatedUpdatedSoftDeleteMixin):
    first_name = models.CharField(max_length=100, help_text=_("User's first name"))
    last_name = models.CharField(max_length=100, help_text=_("User's last name"))
    mobile_number = PhoneNumberField(unique=True, blank=True, null=True, help_text=_("User's Mobile Number"))
    email = models.EmailField(unique=True, help_text=_("User's Email"))
    is_email_verified = models.BooleanField(default=False, help_text=_("Is User's Email Verified"))
    is_mobile_verified = models.BooleanField(default=False, help_text=_("Is User's Mobile Verified"))
    is_staff = models.BooleanField(default=False, help_text=_("Is User Admin"))
    is_superuser = models.BooleanField(default=False, help_text=_("Is User a SuperUser"))
    profile_picture = models.ImageField(
        upload_to=profile_picture_upload,
        default=settings.DEFAULT_USER_IMAGE_PATH,
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.ALLOWED_FILE_EXTENSION_FOR_IMAGE,
            ),
            file_size_validator,
        ],
        help_text=_("Profile Image for a User"),
    )
    otp_secret_key = models.CharField(max_length=100, help_text=_("User's OTP Secret Key"), unique=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        ordering = [
            "-id",
        ]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.id} | {self.email}"

    def otp_hex(self):
        secret_otp_key = pyotp.random_base32(256)
        return secret_otp_key

    def save(self, *args, **kwargs):
        self.otp_secret_key = self.otp_hex()
        super(User, self).save(*args, **kwargs)

    def otp(self, otp=None, validate=False, generate=False) -> bool or int:
        """
        Validate the one time password.
        """
        otp_secret_key = self.otp_secret_key
        totp = pyotp.TOTP(otp_secret_key, interval=600)
        if validate:
            return totp.verify(otp)
        if generate:
            return totp.now()
        return False

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def get_profile_picture(self) -> str:
        if self.profile_picture and os.path.isfile(self.profile_picture.path):
            return self.profile_picture.url
        else:
            file_name = settings.DEFAULT_USER_IMAGE_PATH
            file_url = urllib.parse.urljoin(settings.API_BASE_URL, static(file_name))
            return file_url
