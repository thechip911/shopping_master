from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.forms import UserCreationForm
from core_libs.admin_fields import BaseAdminReadOnlyFields

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseAdminReadOnlyFields):
    form = UserCreationForm
    list_display = ("id", "name", "email", "is_staff", "is_superuser", "is_deleted")
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
