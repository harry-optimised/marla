from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "api_key", "is_staff")
    search_fields = ("username", "email", "api_key")

    readonly_fields = ("api_key",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "api_key",
                    "is_staff",
                    "is_premium",
                    "remaining_questions",
                    "stripe_customer_id",
                )
            },
        ),
    )
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
