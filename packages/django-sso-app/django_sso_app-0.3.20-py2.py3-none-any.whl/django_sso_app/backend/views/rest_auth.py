import logging
from urllib.parse import urlencode

from allauth.account.adapter import get_adapter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from rest_auth.registration.views import RegisterView as rest_authRegisterView
from rest_auth.registration.views import \
    VerifyEmailView as rest_authVerifyEmailView
from rest_auth.views import LoginView as rest_authLoginView
from rest_auth.views import LogoutView as rest_authLogoutView
from rest_auth.views import PasswordChangeView as rest_authPasswordChangeView
from rest_auth.views import \
    PasswordResetConfirmView as rest_authPasswordResetConfirmView
from rest_auth.views import PasswordResetView as rest_authPasswordResetView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django_sso_app.core.apps.passepartout.models import Passepartout
from django_sso_app.core.apps.users.serializers import UserSerializer
from django_sso_app.core.permissions import is_staff
from ..handlers import jwt_encode
from ..serializers import JWTSerializer
from ..utils import set_cookie, invalidate_cookie, get_request_jwt_fingerprint

logger = logging.getLogger('backend')


# rest_auth views

class RegisterAPIView(rest_authRegisterView):
    """
    Register a new user
    """

    def create(self, request, *args, **kwargs):
        try:
            logger.info('Registering user {}'.format(request.data))
            return super(RegisterAPIView, self).create(request, *args, **kwargs)

        except:
            logger.exception('Registration error')
            raise


class VerifyEmailAPIView(rest_authVerifyEmailView):
    """
    Verify new user email
    """

    def post(self, request, *args, **kwargs):
        logger.info('Verifying email')
        try:
            return super(VerifyEmailAPIView, self).post(request, *args,
                                                        **kwargs)
        except:
            logger.exception('Email verification error')
            raise


class LoginAPIView(rest_authLoginView):
    """
    User login
    """

    def return_unauthorized_if_user_is_staff(self):
        if self.user.is_staff:
            logger.warning('Staff user {0} tried to login'.format(self.user))
            return Response('Login unauthorized',
                            status=status.HTTP_403_FORBIDDEN)
        return None

    def get_device(self, fingerprint):
        device = self.user.devices.filter(fingerprint=fingerprint).first()
        adapter = get_adapter(self.request)

        if device is None:
            logger.info('User {0} Login with new Device fingerprint {1}'.format(
                self.user, fingerprint))
            device = adapter.add_user_device(self.user, fingerprint)

        assert device is not None

        setattr(self, 'device', device)

        return device

    def get_response(self):
        # check uesr is not staff
        failing_response = self.return_unauthorized_if_user_is_staff()
        if failing_response is not None:
            return failing_response

        passepartout_url = None

        if settings.DJANGO_SSO_PASSEPARTOUT_PROCESS_ENABLED:
            logger.info(
                'Passepartout login enabled, DJANGO_SSO_URLS_CHAIN: {0}'.format(
                    settings.DJANGO_SSO_URLS_CHAIN))
            nextUrl = self.request.GET.get('next', None)
            if nextUrl is None:
                nextUrl = settings.APP_URL

            fingerprint = self.serializer.validated_data.get('fingerprint', self.request.data.get('fingerprint',
                                                                                                  'undefined'))
            device = self.get_device(fingerprint)

            logger.info(
                'Login started passepartout logic'
                'for user {0}, with device {1}, nextUrl is {2}'.format(
                    self.user, device, nextUrl))

            passepartout = Passepartout.objects.create_passepartout(
                device=device, jwt=self.token)
            logger.info('Created passepartout object {0}'.format(passepartout))

            args = {
                'next': nextUrl
            }
            next_sso_service = settings.DJANGO_SSO_URLS_CHAIN[0]

            redirect_to = next_sso_service + reverse(
                'passepartout:passepartout_login',
                args=(passepartout.token,)) + '?' + urlencode(args)

            passepartout_url = redirect_to

        else:
            logger.info('Only one SSO instance, no passepartout process')

        data = {
            'user': self.user,
            'token': self.token,
            'passepartout_redirect_url': passepartout_url
        }
        serializer = JWTSerializer(instance=data,
                                   context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        set_cookie(response, 'jwt', self.token, None)

        return response

    def login(self, *args, **kwargs):
        self.user = self.serializer.validated_data['user']

        if is_staff(self.user):
            logger.info(
                'User {0} is staff, returning.'.format(self.user))
            return

        # print('\n\nCI SONO!!', self.request.data)
        #print('DATAAAS??', self.request.data, self.request.data.get('fingerprint'))
        # fingerprint = self.serializer.validated_data['fingerprint']
        fingerprint = self.serializer.validated_data.get('fingerprint', self.request.data.get('fingerprint'))

        logger.info(
            'Start logging in user {0} with fingerprint {1}'.format(self.user,
                                                                    fingerprint))

        if self.user.apigw_consumer_id is None:
            logger.info(
                'User {} is logging in for the first time, creating apigw '
                'consumer'.format(
                    self.user))
            adapter = get_adapter()
            adapter.create_apigw_consumer(self.user)

        device = self.get_device(fingerprint)

        self.token = jwt_encode(self.user, device=device)

        logger.info('User {0} is logging in with device {1}'.format(self.user,
                                                                    self.device))

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def post(self, request, *args, **kwargs):
        try:
            return super(LoginAPIView, self).post(request, *args, **kwargs)
        except:
            logger.exception('Login error')
            raise


class LogoutAPIView(rest_authLogoutView):
    """
    Calls Django logout method and deletes the Token object
    assigned to the current User object.

    post:
    Accepts "next" url parameter
    Returns a JSON object containing logout detail message and, if there are
    more than one django-sso instances, a passepartout redirect url.
    """

    def logout(self, request):

        if settings.DJANGO_SSO_PASSEPARTOUT_PROCESS_ENABLED:
            logger.info(
                'Passepartout logout enabled, DJANGO_SSO_URLS_CHAIN: {0}'.format(
                    settings.DJANGO_SSO_URLS_CHAIN))
            nextUrl = self.request.GET.get('next', None)
            if nextUrl is None:
                nextUrl = settings.APP_URL

            args = {
                'next': nextUrl
            }

            requesting_device_fingerprint = get_request_jwt_fingerprint(request)
            device = request.user.devices.filter(
                fingerprint=requesting_device_fingerprint).first()

            assert device is not None

            next_sso_service = settings.DJANGO_SSO_URLS_CHAIN[0]
            redirect_to = next_sso_service + reverse(
                'passepartout:passepartout_logout',
                args=[device.id]) + '?' + urlencode(args)

            response_object = {"detail": _("Successfully logged out."),
                               "passepartout_redirect_url": redirect_to}
            response = Response(response_object, status=status.HTTP_200_OK)
        else:
            if not settings.DEBUG:
                adapter = get_adapter(self.request)

                try:
                    adapter.delete_request_device(request)
                except KeyError as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

            response = super(LogoutAPIView, self).logout(request)

        invalidate_cookie(response)

        return response

    def post(self, request, *args, **kwargs):
        try:
            return super(LogoutAPIView, self).post(request, *args, **kwargs)
        except:
            logger.exception('Logout error')
            raise


class UserDetailsAPIView(RetrieveAPIView):
    """
    Overrides django-rest-auth default UserDetailsView
    in order to prevent PATCH
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        https://github.com/Tivix/django-rest-auth/issues/275
        """
        return get_user_model().objects.none()

    def get(self, request, *args, **kwargs):
        try:
            return super(UserDetailsAPIView, self).get(request, *args, **kwargs)
        except:
            logger.exception('Error getting user details')
            raise


class PasswordResetAPIView(rest_authPasswordResetView):
    """
    Reset password
    """

    def post(self, request, *args, **kwargs):
        logger.info('Asking for password reset')
        try:
            return super(PasswordResetAPIView, self).post(request, *args,
                                                          **kwargs)
        except:
            logger.exception('Error while asking password reset')
            raise


class PasswordResetConfirmAPIView(rest_authPasswordResetConfirmView):
    """
    Password reset confirmation
    """

    def post(self, request, *args, **kwargs):
        logger.info('Confirming password reset')
        try:
            return super(PasswordResetConfirmAPIView, self).post(request, *args,
                                                                 **kwargs)
        except:
            logger.exception('Error resetting password')
            raise


class PasswordChangeAPIView(rest_authPasswordChangeView):
    """
    Password change
    """

    def post(self, request, *args, **kwargs):
        logger.info('Changing password')
        try:
            return super(PasswordChangeAPIView, self).post(request, *args,
                                                           **kwargs)
        except:
            logger.exception('Error changing password')
            raise
