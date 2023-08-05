from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UsersConfig(AppConfig):
    name = "django_sso_app.backend.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import django_sso_app.backend.users.signals  # noqa F401
            if settings.DJANGO_SSO_BACKEND_ENABLED:
                import django_sso_app.core.apps.users.signals  # noqa F401
        except ImportError:
            pass
