from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Поля, які будуть відображатися у списку користувачів в адмінці
    list_display = ("email", "full_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "full_name", "username")
    ordering = ("email",)
    readonly_fields = ("date_joined",)

    # Поля, які використовуються для створення/редагування користувача в адмінці
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Особисті дані"), {"fields": ("full_name", "username", "phone_number", "role")}),
        (
            _("Права доступу"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Важливі дати"), {"fields": ("date_joined", "last_login")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "password1", "password2", "is_staff", "is_active", "role"),
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions")
