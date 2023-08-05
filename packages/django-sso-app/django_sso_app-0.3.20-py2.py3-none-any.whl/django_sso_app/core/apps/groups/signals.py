import logging

from django.conf import settings
from django.contrib.auth.models import Group as GroupModel
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Group
from ..api_gateway.functions import create_consumer_acl, delete_consumer_acl

logger = logging.getLogger('groups')


def create_user_group(user, group):
    logger.info('creating user group {} for {}'.format(group, user))
    if settings.TESTING_MODE:
        return True

    if settings.DJANGO_SSO_BACKEND_ENABLED:
        if settings.DJANGO_SSO_APIGW_ENABLED:
            status_code, resp = create_consumer_acl(user, group.name)
            logger.info('CREATED {}, {}'.format(status_code, resp))
            return True

    return True


def delete_user_group(user, group):
    logger.info('deleting user group {} for {}'.format(group, user))
    if settings.TESTING_MODE:
        return True

    if settings.DJANGO_SSO_BACKEND_ENABLED:
        if settings.DJANGO_SSO_APIGW_ENABLED:
            status_code, resp = delete_consumer_acl(user, group.name)
            logger.info('DELETED {}'.format(status_code))
            return True

    return True


@receiver(m2m_changed)
def signal_handler_when_user_is_added_or_removed_from_group(action, instance, pk_set, model, **kwargs):
    if model == GroupModel:
        user = instance
        user_updated = False
        if action == 'pre_add':
            for pk in pk_set:
                group = Group.objects.get(id=pk)
                user_updated = create_user_group(user, group)
        elif action == 'pre_remove':
            for pk in pk_set:
                group = Group.objects.get(id=pk)
                user_updated = delete_user_group(user, group)
        if user_updated:
            user.update_rev(True)
