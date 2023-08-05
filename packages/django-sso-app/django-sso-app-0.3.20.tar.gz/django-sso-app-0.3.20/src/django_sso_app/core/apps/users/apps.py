from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'django_sso_app.core.apps.users'

    def __init__(self, *args, **kwargs):
        ret = super(UsersConfig, self).__init__(*args, **kwargs)
        print('eccolo', self.label)
        return ret

    def ready(self):
        try:
            import django_sso_app.core.apps.users.signals  # noqa F401
        except ImportError:
            pass
