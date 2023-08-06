import logging
import uuid

from django.utils.translation import activate as activate_translation
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from allauth.account.adapter import DefaultAccountAdapter

from django_sso_app.core.apps.devices.models import Device
from django_sso_app.core.apps.services.models import Service, Subscription
from django_sso_app.core.utils import get_random_string, get_profile_model
from django_sso_app.backend.utils import get_request_jwt_fingerprint
from django_sso_app.core.apps.api_gateway.functions import create_consumer_jwt, create_consumer, create_consumer_acl

logger = logging.getLogger('backend')
Profile = get_profile_model()


class UserAdapter(DefaultAccountAdapter):

    def update_user_profile(self, user, cleaned_data, commit=True):
        logger.info(
            'Updating profile fields for {0}: {1}'.format(user, cleaned_data))

        profile = user.sso_app_profile
        if profile is None:
            logger.info('No profile.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        for f in settings.DJANGO_SSO_PROFILE_FIELDS:
            data = cleaned_data.get(f, None)
            logger.info('SAVING profile FIELD: {}. Data: {}'.format(f, data))
            setattr(profile, f, data)

        if commit:
            profile.save()

        return profile

    def new_user(self, request):
        """
        Instantiates a new User instance.
        """
        new_user_sso_id = uuid.uuid4()
        new_user = get_user_model()(sso_id=new_user_sso_id)

        return new_user

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        # !atomic
        new_user = super(UserAdapter, self).save_user(
            request, user, form, False)

        cleaned_data = form.get_cleaned_data()
        logger.info(
            'Saving new user {0} with email {1} from form {2} with cleaned_data {3}'.format(cleaned_data.get('username'), cleaned_data.get('email'), form.__class__, cleaned_data))

        has_profile = True
        try:
            _profile = new_user.sso_app_profile
        except ObjectDoesNotExist:
            has_profile = False

        if not has_profile:
            new_user.save()

        """
        for field in settings.DJANGO_SSO_USER_FIELDS + ('is_unsubscribed', ):
            data = cleaned_data.get(field, None)

            logger.info('SAVING USER FIELD: {}. Data: {}'.format(field, data))
            setattr(new_user, field, data)

        if not settings.ACCOUNT_USERNAME_REQUIRED and not new_user.username:
            logger.info('SETTING USERNAME AS EMAIL {}'.format({new_user.email}))
            new_user.username = new_user.email
        """

        self.update_user_profile(new_user, cleaned_data, commit or has_profile)

        if commit:
            new_user.save()
        # !endatomic

        return new_user

    def render_mail(self, template_prefix, email, context):
        user = context.get('user')
        user_language = user.sso_app_profile.language
        logger.info('Rendering mail for {0} with language {1}'.format(user, user_language))
        activate_translation(user_language)
        context.update({
            'EMAILS_DOMAIN': settings.EMAILS_DOMAIN,
            'EMAILS_SITE_NAME': settings.EMAILS_SITE_NAME
        })
        return super(UserAdapter, self).render_mail(template_prefix, email, context)

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.
        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(
            "account_confirm_email",
            args=[emailconfirmation.key])
        ret = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL + "://" + settings.EMAILS_DOMAIN + url
        return ret

    # pai

    def add_user_device(self, user, fingerprint, user_agent=None):
        logger.info(
            'Adding User Device for user {0} with fingerprint {1}'.format(user,
                                                                          fingerprint))

        device = Device(user=user, fingerprint=fingerprint)

        if not settings.TESTING_MODE:
            status_code, r1 = create_consumer_jwt(self)
            if status_code != 201:
                # delete_apigw_consumer(username)
                logger.error(
                    'Error ({0}) creating apigw consumer JWT, {1}'.format(
                        status_code, r1))
                raise Exception(
                    "Error creating apigw consumer jwt, {}".format(status_code))

            device.apigw_jwt_id = r1.get('id')
            device.apigw_jwt_key = r1.get('key')
            device.apigw_jwt_secret = r1.get('secret')

        else:
            device.apigw_jwt_id = get_random_string(36)
            device.apigw_jwt_key = get_random_string(32)
            device.apigw_jwt_secret = get_random_string(32)

        device.save()

        return device

    def remove_user_device(self, device):
        logger.info('Removing Device {0}'.format(device.id))
        device.delete()
        return 1

    def remove_all_user_devices(self, user):
        logger.info('Removing All User Devices for {0}'.format(user))
        removed = 0
        for d in user.devices.all():
            removed += self.remove_user_device(d)
        return removed

    def subscribe_to_service(self, user, referrer, update_rev=False, commit=True):
        logger.info('Subscribinig {0} to service {1}'.format(user, referrer))

        service = Service.objects.get(url=referrer)

        subscription, _subscription_created = \
            Subscription.objects.get_or_create(
                user=user, service=service)

        if _subscription_created:
            logger.info('Created service subscrption for {0}'.format(user))
            if update_rev:
                setattr(user, '__subscription_updated', True)
                user.update_rev(commit)
        else:
            logger.info(
                'User {0} already subscribed to {1}'.format(user, service))

        return _subscription_created

    def unsubscribe_from_service(self, user, subscription, update_rev=False,
                                 commit=True):
        logger.info('Unubscribinig {0} form service {1}'.format(user,
                                                                subscription.service))
        setattr(user, '__subscription_updated', True)

        subscription.unsubscribed_at = timezone.now()
        subscription.save()

        if update_rev:
            user.update_rev(commit)

    def create_apigw_consumer(self, user):
        logger.info('Adding apigw consumer for User {0}'.format(user))
        if not settings.TESTING_MODE:
            status_code_1, consumer = create_consumer(user)
            if status_code_1 != 201:
                logger.error('Error ({0}) creating apigw consumer, {1}'.format(
                    status_code_1, consumer))
                raise Exception(
                    "Error ({0}) creating apigw consumer, {1}".format(
                        status_code_1, consumer))

            status_code_2, acl = create_consumer_acl(user)
            if status_code_2 != 201:
                # delete_apigw_consumer(username)
                logger.error(
                    'Error ({0}) creating apigw consumer acl, {1}'.format(
                        status_code_2, acl))
                raise Exception(
                    "Error {0} creating apigw consumer acl, {1}".format(
                        status_code_2, acl))
            user.apigw_consumer_id = consumer['id']

        else:
            user.apigw_consumer_id = get_random_string(36)

        user.save()

    def get_request_device(self, request):
        received_jwt = get_request_jwt_fingerprint(request)
        return Device.objects.filter(fingerprint=received_jwt).first()

    def delete_request_device(self, request):
        removing_device = self.get_request_device(request)
        if removing_device is not None:
            logger.info('Removing logged out user device {0} for User {1}'.format(removing_device, request.user))
            self.remove_user_device(removing_device)
        else:
            logger.warning('User {0} is logging out WITHOUT removing device.'.format(request.user))

