import logging
import random
import string
from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model
from six import string_types

logger = logging.getLogger("utils")


def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)


def get_profile_model():
    profile_model = getattr(settings, 'DJANGO_SSO_APP_USER_PROFILE_MODEL', None)
    if profile_model is None:
        return get_user_model()
    else:
        return import_callable(profile_model)


def get_country_language(country):
    logger.debug('Getting language for country {}'.format(country))
    if country == 'IT':
        return 'it'
    elif country == 'BR' or country == 'PT':
        return 'pt'
    elif country == 'ES':
        return 'es'

    return 'en-gb'


def get_random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
