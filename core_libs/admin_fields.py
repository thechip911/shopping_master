from django.contrib.admin import ModelAdmin


class BaseAdminReadOnlyFields(ModelAdmin):
    list_filter = ("is_deleted",)
    readonly_fields = (
        "created_by_id",
        "updated_by_id",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    def get_queryset(self, request):
        return self.model.all_objects
