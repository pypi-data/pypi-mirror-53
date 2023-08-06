import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from django_sso_app.core.utils import get_profile_model

logger = logging.getLogger('profiles')
Profile = get_profile_model()


@receiver(post_save, sender=Profile)
def profile_updated(sender, instance, created, **kwargs):
    if settings.DJANGO_SSO_BACKEND_ENABLED:
        if not created:
            logger.info('Profile updated for {}, updating user revision {}.'.format(instance.user, instance.sso_rev))

            setattr(instance.user, '__profile_field_updated', True)
            instance.user.update_rev(True)
