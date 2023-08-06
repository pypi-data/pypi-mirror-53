import logging
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from allauth.account.adapter import get_adapter

from django_sso_app.core.apps.api_gateway.functions import delete_consumer
from django_sso_app.core.utils import get_profile_model

logger = logging.getLogger('users')
User = get_user_model()
Profile = get_profile_model()


@receiver(pre_save, sender=User)
def check_upated_fields(sender, instance, **kwargs):
    if not instance._state.adding:  # if instance.pk:
        profile_field_updated = hasattr(instance, '__profile_field_updated')
        email_updated = hasattr(instance, '__email_updated')
        subscription_updated = hasattr(instance, '__subscription_updated') or instance.is_unsubscribed
        password_updated = hasattr(instance, '__password_updated')
        field_updated = instance.__serialized_as_string != \
                        instance.serialized_as_string()

        update_rev = False

        if field_updated:
            logger.info('User {0} updated DJANGO_SSO_USER_FIELDS \n{1}\n{2}'.format(instance, instance.__serialized_as_string, instance.serialized_as_string()))
            update_rev = True

        if profile_field_updated:
            logger.info('User {0} updated DJANGO_SSO_PROFILE_FIELDS')
            update_rev = True

        if email_updated:
            logger.info('User {0} updated email'.format(instance))

        if password_updated:
            logger.info('User {0} updated password'.format(instance))

        if subscription_updated:
            logger.info('User {0} updated subscription'.format(instance))

        if email_updated or password_updated or field_updated or subscription_updated:
            # __password_hardened attribute set by
            # backend.serializers.LoginSerializer on runtime password hardening
            update_rev = True

        if hasattr(instance, '__password_hardened'):
            update_rev = False

        if update_rev:
            instance.update_rev()  # updating rev
            setattr(instance, '__rev_updated', True)

            logger.info('rev updated, removing all devices for user {}.'.format(instance))
            adapter = get_adapter()
            adapter.remove_all_user_devices(instance)


@receiver(post_save, sender=User)
def fetch_from_db_if_updated(sender, instance, created, **kwargs):
    if settings.DJANGO_SSO_APP_USES_EXTERNAL_USER_PROFILE:
        try:
            instance.sso_app_profile
        except ObjectDoesNotExist:
            logger.info('User {0} has no profile, creating one.'.format(instance))
            Profile.objects.create(user=instance, sso_id=instance.sso_id, sso_rev=0)

    if not created:
        if hasattr(instance, '__rev_updated'):
            logger.info('User {0} updated rev, refreshing instance from DB'.format(instance))
            instance.refresh_from_db()


@receiver(pre_delete, sender=User)
def delete_apigw_user_consumer(sender, instance, **kwargs):
    logger.info('Deleting apigw Consumer for User {0}'.format(instance))
    if not settings.TESTING_MODE:
        status_code, r1 = delete_consumer(instance)
        logger.info('Kong consumer deleted ({0}), {1}'.format(status_code, r1))
        if status_code >= 300:
            if status_code != 404:
                # delete_apigw_consumer(username)
                logger.error(
                    'Error ({0}) Deleting apigw consumer for User {1}, {2}'.format(
                        status_code, instance, r1))
                raise Exception(
                    "Error deleting apigw consumer, {}".format(status_code))
