import logging

from django.conf import settings
from rest_framework import authentication

from django_sso_app.core.utils import get_profile_model
from .utils import create_local_profile_from_headers, get_sso_id

logger = logging.getLogger('app')
Profile = get_profile_model()


def get_apigw_user(request):
    is_anonymous = request.META.get(settings.DJANGO_SSO_ANONYMOUS_CONSUMER_HEADER, None) is not None
    apigw_consumer_id = get_sso_id(
        request.META.get(settings.DJANGO_SSO_CONSUMER_USERNAME_HEADER, settings.DJANGO_SSO_ANONYMOUS_CONSUMER_USERNAME))

    logger.debug('Got apigw_consumer_id: {}'.format(apigw_consumer_id))

    # Consumer is anonymous
    if is_anonymous or apigw_consumer_id == settings.DJANGO_SSO_ANONYMOUS_CONSUMER_USERNAME:
        logger.info('Apigw says user is anonymous')
        return

    try:
        user_profile = Profile.objects.get(sso_id=apigw_consumer_id)
        user = user_profile.user
        if settings.DJANGO_SSO_APP_USES_EXTERNAL_USER_PROFILE:
            user = user_profile.user

    except Profile.DoesNotExist:
        logger.info(
            'User with sso_id: {} does not exists, creating new one'.format(apigw_consumer_id))
        user = create_local_profile_from_headers(request)

    finally:
        return user


class DjangoSsoAppAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user = get_apigw_user(request)
        logger.info('DjangoSsoAppAuthentication: authenticated as {}'.format(user))
        return user, None
