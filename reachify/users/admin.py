from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import decorators
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from reachify.users.forms import UserAdminChangeForm
from reachify.users.forms import UserAdminCreationForm
from reachify.users.models import Member

User = get_user_model()

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]

admin.site.site_header = 'Reachify Admin'
admin.site.site_title = 'Welcome to Reachify Admin'
admin.site.index_title = 'Reachify Admin'


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
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
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["username", "user", "used_credit", "is_active", "created"]
    readonly_fields = ['created']
