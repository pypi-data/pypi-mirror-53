from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        #if obj is None:
        return ['sso_id', 'sso_rev']


admin.site.register(Profile, ProfileAdmin)
