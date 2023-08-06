import logging

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_sso_app.core.permissions import is_staff
from django_sso_app.core.serializers import AbsoluteUrlSerializer
from django_sso_app.core.utils import get_profile_model

logger = logging.getLogger('users')
User = get_user_model()
Profile = get_profile_model()


class CheckUserExistenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('sso_id',)
        read_only_fields = ('sso_id',)


class UserSerializer(AbsoluteUrlSerializer):
    subscriptions = serializers.SerializerMethodField(required=False)
    email_verified = serializers.SerializerMethodField(required=False)

    groups = serializers.SerializerMethodField(required=False)

    profile = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        read_only_fields = (
            'url',
            'sso_id', 'sso_rev', 'date_joined', 'username', 'is_unsubscribed',
            'is_active', 'subscriptions', 'email_verified',
            'groups',
            'profile')
        fields = read_only_fields

    def get_subscriptions(self, instance):
        serialized = []
        for el in instance.subscriptions.all():
            serialized.append({
                'url': el.service.url,
                'is_unsubscribed': el.is_unsubscribed
            })
        return serialized

    def get_email_verified(self, instance):
        if is_staff(instance):
            return True
        try:
            email_address = instance.emailaddress_set.get(email=instance.email)
            return email_address.verified
        except:
            logger.info('{} has not verified email.'.format(instance))
            pass
        finally:
            return False

    def get_groups(self, instance):
        groups = list(instance.groups.values_list('name', flat=True))

        return groups

    def get_profile(self, instance):
        if settings.DJANGO_SSO_APP_USES_EXTERNAL_USER_PROFILE:
            profile = instance.sso_app_profile
            request = self.context['request']
            return request.build_absolute_uri(profile.get_absolute_url())

    def update(self, instance, validated_data):
        user = instance
        request = self.context.get("request")
        requesting_user = request.user
        requesting_user_is_staff = is_staff(requesting_user)
        skip_confirmation = request.GET.get('skip_confirmation', None)
        must_confirm_email = True

        logger.info(
            'User {0} wants to update user {1}: {2}'.format(requesting_user, user, validated_data))

        if requesting_user_is_staff and skip_confirmation is not None:
            must_confirm_email = False

        new_email = validated_data.get('email', None)
        if (new_email is not None):

            if new_email == user.email:  # !! because of app shitty logic (
                # always sends all fields)
                logger.info('{0} is has same email'.format(user))

            else:
                logger.info(
                    '{0} is changing email for user {1}, email confirmation '
                    'is {2}'.format(
                        requesting_user, user, must_confirm_email))

                adapter = get_adapter(request=request)

                created_email = EmailAddress.objects.add_email(request, user,
                                                               new_email,
                                                               confirm=must_confirm_email)
                logger.info(
                    'A new EmailAddress for {0} has been created with id {1}'
                    ''.format(
                        new_email, created_email.id))

                if must_confirm_email:
                    if requesting_user_is_staff:
                        logger.info(
                            'deactivating all emails for {0} while email has been updated by staff user {1}'.format(user,
                                                                                                               requesting_user))

                        # EmailAddress.objects.filter(user=user, primary=True).update(primary=False)
                        # setattr(request.session, 'account_verified_email', None)
                        setattr(user, '__email_updated', new_email)

                    logger.info(
                        '{0} must confirm email {1}'.format(user, new_email))
                else:
                    adapter.confirm_email(None, created_email)

                setattr(user, '__email_updated', True)

        new_password = validated_data.get('password', None)
        if (new_password is not None):
            logger.info(
                '{0} is changing password for user {1}'.format(requesting_user,
                                                               user))
            validated_data.pop(
                'password')  # serializer must NOT save the received plain
            # password, password update logic performed by user.set_password

            user.set_password(new_password)

        # devices will be removed by signal
        # actual_devices = user.devices.all()
        # actual_devices_count = actual_devices.count()
        # deleted_devices = user.remove_all_user_devices()

        return super(UserSerializer, self).update(instance, validated_data)

    def to_representation(self, obj):
        # get the original representation
        ret = super(UserSerializer, self).to_representation(obj)
        req = self.context.get('request', None)

        if req is not None:
            # remove field if password if not asked
            with_pass = req.query_params.get('with_password',
                                             not settings.DJANGO_SSO_HIDE_PASSWORD_FROM_USER_SERIALIZER)

            if not with_pass:
                ret.pop('password', None)

        # return the modified representation
        return ret


class UserUpdateSerializer(UserSerializer):
    class Meta:
        model = User
        read_only_fields = (
            'url',
            'sso_id', 'sso_rev', 'date_joined', 'username', 'is_unsubscribed',
            'is_active', 'subscriptions', 'email_verified',
            'groups',
            'profile')
        fields = read_only_fields + ('username', 'email', 'password')

    def update(self, instance, validated_data):
        user = instance
        request = self.context.get("request")
        requesting_user = request.user
        requesting_user_is_staff = is_staff(requesting_user)
        skip_confirmation = request.GET.get('skip_confirmation', None)
        must_confirm_email = True

        logger.info(
            'User {0} wants to update user {1}: {2}'.format(requesting_user, user, validated_data))

        if requesting_user_is_staff and skip_confirmation is not None:
            must_confirm_email = False

        new_email = validated_data.get('email', None)
        if (new_email is not None):

            if new_email == user.email:  # !! because of app shitty logic (
                # always sends all fields)
                logger.info('{0} is has same email'.format(user))

            else:
                logger.info(
                    '{0} is changing email for user {1}, email confirmation '
                    'is {2}'.format(
                        requesting_user, user, must_confirm_email))

                adapter = get_adapter(request)

                created_email = EmailAddress.objects.add_email(request, user,
                                                               new_email,
                                                               confirm=must_confirm_email)
                logger.info(
                    'A new EmailAddress for {0} has been created with id {1}'
                    ''.format(
                        new_email, created_email.id))

                if must_confirm_email:
                    if requesting_user_is_staff:
                        logger.info(
                            'deactivating all emails for {0} while email has been updated by staff user {1}'.format(user,
                                                                                                               requesting_user))

                        # EmailAddress.objects.filter(user=user, primary=True).update(primary=False)
                        # setattr(request.session, 'account_verified_email', None)
                        setattr(user, '__email_updated', new_email)

                    logger.info(
                        '{0} must confirm email {1}'.format(user, new_email))
                else:
                    adapter.confirm_email(None, created_email)

                setattr(user, '__email_updated', True)


        new_password = validated_data.get('password', None)
        if (new_password is not None):
            logger.info(
                '{0} is changing password for user {1}'.format(requesting_user,
                                                               user))

            password_is_hashed = request.query_params.get('password_is_hashed', None)
            if password_is_hashed:
                user.password = new_password
            else:
                user.set_password(new_password)
            validated_data.pop(
                'password')  # serializer must NOT save the received plain
            # password, password update logic performed by user.set_password

        # devices will be removed by signal
        # actual_devices = user.devices.all()
        # actual_devices_count = actual_devices.count()
        # deleted_devices = user.remove_all_user_devices()

        return super(UserSerializer, self).update(instance, validated_data)


class UserUnsubscriptionSerializer(serializers.Serializer):
    password = serializers.CharField()


class UserRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('sso_id', 'sso_rev')
        fields = read_only_fields
