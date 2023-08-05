from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.conf import settings

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


if settings.DJANGO_SSO_BACKEND_ENABLED or settings.DJANGO_SSO_APP_ENABLED:
    from django_sso_app.core.utils import get_profile_model

    if settings.DJANGO_SSO_BACKEND_ENABLED:
        _list_display = ["username", "email", "is_superuser", "sso_id", "sso_rev"]
        _search_fields = ["username", "email", "sso_id"]
    elif settings.DJANGO_SSO_APP_ENABLED:
        _list_display = ["username", "email", "is_superuser"]
        _search_fields = ["username", "email"]

    Profile = get_profile_model()

    class ProfileInline(admin.StackedInline):
        model = Profile
        max_num = 1
        can_delete = False

        def get_readonly_fields(self, request, obj=None):
            # if obj is None:
            return ['sso_id', 'sso_rev']


    @admin.register(User)
    class UserAdmin(auth_admin.UserAdmin):
        form = UserChangeForm
        add_form = UserCreationForm

        # pai
        # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
        fieldsets = auth_admin.UserAdmin.fieldsets
        list_display = _list_display
        search_fields = _search_fields

        # pai
        inlines = [ProfileInline]

else:
    @admin.register(User)
    class UserAdmin(auth_admin.UserAdmin):
        form = UserChangeForm
        add_form = UserCreationForm

        # pai
        # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
        fieldsets = auth_admin.UserAdmin.fieldsets
        list_display = ["username", "email", "is_superuser"]
        search_fields = ["username", "email"]

