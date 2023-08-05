from django.apps import AppConfig
from django.conf import settings

if settings.DJANGO_SSO_BACKEND_ENABLED:
    from django_sso_app.core.apps.profiles.apps import ProfilesConfig as DjangoSSoAppProfilesConfig

    class ProfilesConfig(DjangoSSoAppProfilesConfig):
        name = 'django_sso_app.backend.profiles'
else:
    class ProfilesConfig(AppConfig):
        name = 'backend.profiles'
