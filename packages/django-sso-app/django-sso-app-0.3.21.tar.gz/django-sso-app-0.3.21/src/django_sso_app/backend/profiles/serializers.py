from django_sso_app.core.apps.profiles.serializers import ProfilePublicSerializer as DjangoSSoAppProfilePublicSerializer
from django_sso_app.core.apps.profiles.serializers import ProfileSerializer as DjangoSSoAppProfileSerializer


class ProfileSerializer(DjangoSSoAppProfileSerializer):
    pass


class ProfilePublicSerializer(DjangoSSoAppProfilePublicSerializer):
    pass
