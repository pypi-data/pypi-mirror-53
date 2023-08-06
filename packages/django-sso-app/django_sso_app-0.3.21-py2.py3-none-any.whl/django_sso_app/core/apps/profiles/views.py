import logging

from rest_framework import viewsets

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from django_sso_app.backend.utils import get_request_jwt, update_response_jwt
from django_sso_app.core.permissions import is_staff
from django_sso_app.core.utils import get_profile_model

from .forms import ProfileForm
from .serializers import ProfileSerializer, ProfilePublicSerializer

logger = logging.getLogger('profiles')
Profile = get_profile_model()


class ProfileView(TemplateView):
    template_name = "pages/profile.html"

    def get(self, *args, **kwargs):
        logger.info('Getting profile')
        try:
            return super(ProfileView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting profile')
            raise


class ProfileUpdateView(FormView):
    template_name = "pages/profile_update.html"
    form_class = ProfileForm

    def get(self, *args, **kwargs):
        logger.info('Getting profile update')
        try:
            return super(ProfileUpdateView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting profile update')
            raise

    def post(self, *args, **kwargs):
        logger.info('Posting profile update')
        try:
            return super(ProfileUpdateView, self).post(*args, **kwargs)
        except:
            logger.exception('Error posting profile update')
            raise


class ProfileViewSet(viewsets.ModelViewSet):
    lookup_field = 'sso_id'

    def get_queryset(self):
        user = self.request.user
        if is_staff(user):
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return ProfileSerializer
        else:
            return ProfilePublicSerializer

    def list(self, request, *args, **kwargs):
        """
        List profiles
        """
        return super(ProfileViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Profile detail
        """
        return super(ProfileViewSet, self).retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Profile update
        """
        response = super(ProfileViewSet, self).partial_update(request, *args, **kwargs)
        response_status_code = response.status_code
        logger.info('Profile partial_update status code is {}, {}'.format(response_status_code, request.data))

        if response_status_code == 200:
            received_jwt = get_request_jwt(request)
            logger.info('Updating JWT: {}'.format(received_jwt))

            profile = self.get_object()
            user = profile.user
            requesting_user = self.request.user

            from_browser_as_same_user = received_jwt is not None and requesting_user == user
            #logger.info('From browser as same user? {} == {}? {}'. format(requesting_user, user, requesting_user.id == user.id))

            if from_browser_as_same_user: # From browser as same user
                logger.info('User {0} updated profile, updating response JWT'.format(user))
                update_response_jwt(received_jwt, user, request, response)

        return response
