from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.user.models import User
from django.contrib import admin
from django.contrib.auth.models import Group

# Unregister the Group model from the admin site:
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "portfolio_count",
        "date_joined",
        "last_login",
    )
    superuser_list_display = (
        *list_display,
        "is_active",
        "is_staff",
        "is_superuser",
    )
    readonly_fields = (
        "portfolio_count",
        "created",
        "modified",
        "date_joined",
        "last_login",
    )
    main_fieldset = (None, {"fields": ("email", "password")})
    permissions_fieldset = (
        _("Permissions"),
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        },
    )
    important_dates_fieldset = (
        _("Important dates"),
        {
            "fields": (
                "last_login",
                "date_joined",
                "created",
                "modified",
            )
        },
    )
    fieldsets = (
        main_fieldset,
        important_dates_fieldset,
    )
    superuser_fieldsets = (
        main_fieldset,
        permissions_fieldset,
        important_dates_fieldset,
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return User.objects.filter(id=request.user.id)
        return super().get_queryset(request)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.superuser_list_display
        return self.list_display

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return self.superuser_fieldsets
        return self.fieldsets

    def get_search_fields(self, request):
        if request.user.is_superuser:
            return self.search_fields
        return ()

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return ()

    def get_actions(self, request):
        if request.user.is_superuser:
            return super().get_actions(request)
        return ()
