import logging
import os

from allauth.account import views as allauth_account_views
from django.conf import settings
from django.views.generic import TemplateView

logger = logging.getLogger('backend')

CURRENT_DIR = os.getcwd()


# allauth views

class LoginView(allauth_account_views.LoginView):
    def get(self, *args, **kwargs):
        logger.info('Getting login')
        try:
            return super(LoginView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting login')
            raise

    def post(self, *args, **kwargs):
        logger.info('Logging in')
        try:
            return super(LoginView, self).post(*args, **kwargs)
        except:
            logger.exception('Error logging in')
            raise


class SignupView(allauth_account_views.SignupView):
    def get(self, *args, **kwargs):
        logger.info('Getting signup')
        try:
            return super(SignupView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting signup')
            raise

    def post(self, *args, **kwargs):
        logger.info('Signing up')
        try:
            return super(SignupView, self).post(*args, **kwargs)
        except:
            logger.exception('Error signin up')
            raise


class ConfirmEmailView(allauth_account_views.ConfirmEmailView):
    def get(self, *args, **kwargs):
        logger.info('Getting confirm email')
        try:
            return super(ConfirmEmailView, self).get(*args, **kwargs)
        except:
            logger.exception('Error get confirm email')
            raise

    def post(self, *args, **kwargs):
        logger.info('Confirming email')
        try:
            return super(ConfirmEmailView, self).post(*args, **kwargs)
        except:
            logger.exception('Error confirming email')
            raise


class EmailView(allauth_account_views.EmailView):
    def get(self, *args, **kwargs):
        logger.info('Getting email')
        try:
            return super(EmailView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting email')
            raise

    def post(self, *args, **kwargs):
        logger.info('Email')
        try:
            return super(EmailView, self).post(*args, **kwargs)
        except:
            logger.exception('Error email')
            raise


class PasswordChangeView(allauth_account_views.PasswordChangeView):
    def get(self, *args, **kwargs):
        logger.info('Getting password change')
        try:
            return super(PasswordChangeView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting password change')
            raise

    def post(self, *args, **kwargs):
        logger.info('Changing password')
        try:
            return super(PasswordChangeView, self).post(*args, **kwargs)
        except:
            logger.exception('Error changing password')
            raise


class PasswordSetView(allauth_account_views.PasswordSetView):
    def get(self, *args, **kwargs):
        logger.info('Getting password set')
        try:
            return super(PasswordSetView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting password set')
            raise

    def post(self, *args, **kwargs):
        logger.info('Setting password')
        try:
            return super(PasswordSetView, self).post(*args, **kwargs)
        except:
            logger.exception('Error setting password')
            raise


class PasswordResetView(allauth_account_views.PasswordResetView):
    def get(self, *args, **kwargs):
        logger.info('Getting ask password reset')
        try:
            return super(PasswordResetView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting ask password reset')
            raise

    def post(self, *args, **kwargs):
        logger.info('Asking for password reset')
        try:
            return super(PasswordResetView, self).post(*args, **kwargs)
        except:
            logger.exception('Error while asking password reset')
            raise


class PasswordResetDoneView(allauth_account_views.PasswordResetDoneView):
    def get(self, *args, **kwargs):
        logger.info('Getting password reset done')
        try:
            return super(PasswordResetDoneView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting password reset done')
            raise


class PasswordResetFromKeyView(allauth_account_views.PasswordResetFromKeyView):
    def get(self, *args, **kwargs):
        logger.info('Getting password reset from key')
        try:
            return super(PasswordResetFromKeyView, self).get(*args, **kwargs)
        except:
            logger.exception('Error while getting password reset from key')
            raise

    def post(self, *args, **kwargs):
        logger.info('Resetting password form key')
        try:
            return super(PasswordResetFromKeyView, self).post(*args, **kwargs)
        except:
            logger.exception('Error while resetting password form key')
            raise


class PasswordResetFromKeyDoneView(
    allauth_account_views.PasswordResetFromKeyDoneView):
    def get(self, *args, **kwargs):
        logger.info('Getting password reset from key done')
        try:
            return super(PasswordResetFromKeyDoneView, self).get(*args,
                                                                 **kwargs)
        except:
            logger.exception('Error while getting password reset from key done')
            raise


class LogoutView(allauth_account_views.LogoutView):
    def get(self, *args, **kwargs):
        logger.info('Getting logout')
        try:
            return super(LogoutView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting logout')
            raise

    def post(self, *args, **kwargs):
        logger.info('Logging out')
        try:
            return super(LogoutView, self).post(*args, **kwargs)
        except:
            logger.exception('Error logging out')
            raise


class AccountInactiveView(allauth_account_views.AccountInactiveView):
    def get(self, *args, **kwargs):
        logger.info('Getting account inactive')
        try:
            return super(AccountInactiveView, self).get(*args, **kwargs)
        except:
            logger.exception('Error while getting account inactive')
            raise


class EmailVerificationSentView(
    allauth_account_views.EmailVerificationSentView):
    def get(self, *args, **kwargs):
        logger.info('Getting email verification sent')
        try:
            return super(EmailVerificationSentView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting verification sent')
            raise


# custom views

class WebpackBuiltTemplateView(TemplateView):
    """
    Base built template view
    """
    template_name = "frontend/built.html"

    def get_context_data(self, *args, **kwargs):
        context = super(WebpackBuiltTemplateView, self).get_context_data(*args,
                                                                         **kwargs)
        context['COOKIE_DOMAIN'] = settings.COOKIE_DOMAIN
        context['DJANGO_SSO_DEFAULT_REFERRER'] = settings.DJANGO_SSO_DEFAULT_REFERRER
        return context
