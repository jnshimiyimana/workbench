from django.contrib import admin

from workbench.activities.models import Activity


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "contact",
        "project",
        "deal",
        "title",
        "owned_by",
        "due_on",
        "completed_at",
    )
    list_display_links = ("title",)
    raw_id_fields = ("contact", "deal", "project", "owned_by")


admin.site.register(Activity, ActivityAdmin)