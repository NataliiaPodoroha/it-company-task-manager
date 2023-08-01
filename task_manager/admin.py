from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from task_manager.models import Worker, TaskType, Position, Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", "phone_number")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position", "phone_number")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                        "phone_number",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = (
        "is_completed",
        "priority",
        "task_type",
    )


admin.site.register(TaskType)

admin.site.register(Position)
