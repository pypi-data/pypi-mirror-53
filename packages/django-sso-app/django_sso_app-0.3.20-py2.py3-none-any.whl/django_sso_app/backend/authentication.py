import logging

from django.conf import settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


logger = logging.getLogger('backend.authentication')

username_header = getattr(settings, 'DJANGO_SSO_CONSUMER_HEADER', 'HTTP_X_CONSUMER_USERNAME')
anonymous_username = getattr(settings, 'DJANGO_SSO_ANONYMOUS_USERNAME', 'anonymous')


class JWTAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request):
        username = request.META.get(username_header, None)

        if username == anonymous_username:
            logger.info('JWTAuthentication found Anonymous username header set. Skipping authentication.')
            return None
        else:
            return super(JWTAuthentication, self).authenticate(request)
