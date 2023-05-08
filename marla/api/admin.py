from django.contrib import admin

from .models import Context


class ContextAdmin(admin.ModelAdmin):
    list_display = ("get_user", "api_key", "content")
    search_fields = ("api_key",)

    def get_user(self, obj):
        return obj.get_user()

    get_user.short_description = "User"


admin.site.register(Context, ContextAdmin)
