import logging

from django_sso_app.core.apps.profiles.views import (ProfileViewSet as DjangoSSoAppProfileViewSet,
                                                     ProfileView as DjangoSSoAppProfileView,
                                                     ProfileUpdateView as DjangoSSoAppProfileUpdateView)


logger = logging.getLogger('profiles')


class ProfileViewSet(DjangoSSoAppProfileViewSet):
    pass


class ProfileView(DjangoSSoAppProfileView):
    pass


class ProfileUpdateView(DjangoSSoAppProfileUpdateView):
    pass
