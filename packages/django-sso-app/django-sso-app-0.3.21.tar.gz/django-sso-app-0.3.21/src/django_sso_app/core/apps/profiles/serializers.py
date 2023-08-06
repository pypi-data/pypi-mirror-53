import logging

from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse

from django_sso_app.core.serializers import AbsoluteUrlSerializer
from django_sso_app.core.utils import get_profile_model

logger = logging.getLogger('profiles')
Profile = get_profile_model()


class ProfileSerializer(AbsoluteUrlSerializer):
    user = serializers.SerializerMethodField(required=False)
    sso_id = serializers.SerializerMethodField(required=False)
    sso_rev = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Profile
        read_only_fields = (
            'url',
            'created_at',
            'sso_id', 'sso_rev',
            'username', 'email',
            'user') + settings.DJANGO_SSO_USER_FIELDS
        fields = read_only_fields + settings.DJANGO_SSO_PROFILE_FIELDS

    def get_absolute_url(self, obj):
        if getattr(obj, 'id', None) is not None:
            request = self.context['request']
            reverse_url = reverse('profile:detail', args=[obj.sso_id])
            return request.build_absolute_uri(reverse_url)

    def get_user(self, instance):
        try:
            user = instance.user
            request = self.context['request']
            return request.build_absolute_uri(user.get_absolute_url())
        except:
            logger.warning('No profile.user url for {}.'.format(instance))

    def get_sso_id(self, instance):
        if settings.DJANGO_SSO_BACKEND_ENABLED:
            return instance.user.sso_id
        else:
            return instance.sso_id

    def get_sso_rev(self, instance):
        if settings.DJANGO_SSO_BACKEND_ENABLED:
            return instance.user.sso_rev
        else:
            return instance.sso_rev


class ProfilePublicSerializer(ProfileSerializer):

    class Meta:
        model = Profile
        read_only_fields = (
            'url',
            'sso_id',
            'created_at', 'username', 'picture',
            'country')
        fields = read_only_fields
