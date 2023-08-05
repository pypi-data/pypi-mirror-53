import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django_sso_app.core.apps.profiles.models import AbstractUserProfileModel

logger = logging.getLogger('profiles')
User = get_user_model()


class Profile(AbstractUserProfileModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name=_("user"),
                                related_name="sso_app_profile")

    def get_absolute_url(self):
        return reverse("profiles:detail", args=[self.sso_id])
