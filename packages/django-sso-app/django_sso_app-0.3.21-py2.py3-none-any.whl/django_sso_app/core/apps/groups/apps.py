from django.apps import AppConfig


class GroupsConfig(AppConfig):
    name = 'django_sso_app.core.apps.groups'

    def ready(self):
        try:
            import django_sso_app.core.apps.groups.signals  # noqa F401
        except ImportError:
            pass
