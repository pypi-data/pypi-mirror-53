import logging

from django.apps import AppConfig
from django.conf import settings

from django_sso_app.core.utils import get_profile_model

logger = logging.getLogger("profiles")


class ProfilesConfig(AppConfig):
    name = 'django_sso_app.core.apps.profiles'

    def ready(self):
        Profile = get_profile_model()

        for el in settings.DJANGO_SSO_PROFILE_FIELDS:
            if getattr(Profile, el, None) is None:
                raise Exception(
                    'App profile {0} is missing {1} field'.format(Profile,
                                                                  el))

        try:
            import django_sso_app.core.apps.profiles.signals  # noqa F401
        except ImportError:
            pass

        super(ProfilesConfig, self).ready()
        logger.info("django-sso-app profiles app ready!")
