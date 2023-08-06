from django.apps import AppConfig


class DevicesConfig(AppConfig):
    name = 'django_sso_app.core.apps.devices'

    def ready(self):
        try:
            import django_sso_app.core.apps.devices.signals  # noqa F401
        except ImportError:
            pass
