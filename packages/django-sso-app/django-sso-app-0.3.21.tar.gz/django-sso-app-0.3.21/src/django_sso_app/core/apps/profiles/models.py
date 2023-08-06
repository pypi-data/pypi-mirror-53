import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_sso_app.core.models import CreatedAtModel, UpdatableModel, DeactivableModel

logger = logging.getLogger('profiles')


class AbstractUserProfileModel(CreatedAtModel, UpdatableModel, DeactivableModel):
    """
    User profile abstract model
    """

    class Meta:
        abstract = True

    sso_id = models.CharField(max_length=36, unique=True, null=True, blank=True, db_index=True)  # unique on not null
    sso_rev = models.PositiveIntegerField(default=0)

    first_name = models.CharField(_('first name'), max_length=255, null=True,
                                  blank=True)
    last_name = models.CharField(_('last name'), max_length=255, null=True,
                                 blank=True)

    role = models.SmallIntegerField(null=True, blank=True)

    description = models.TextField(_('description'), null=True, blank=True)
    picture = models.TextField(_('picture'), null=True, blank=True)
    birthdate = models.DateField(_('birthdate'), null=True, blank=True)

    latitude = models.FloatField(_('latitude'), null=True, blank=True)
    longitude = models.FloatField(_('longitude'), null=True, blank=True)

    country = models.CharField(_('country'), max_length=46, null=True,
                               blank=True)

    address = models.TextField(_('address'), null=True, blank=True)
    language = models.CharField(_('language'), null=True, blank=True)

    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    language = models.CharField(max_length=3, null=True, blank=True)

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def is_unsubscribed(self):
        return self.unsubscribed_at is not None

    @is_unsubscribed.setter
    def is_unsubscribed(self, value):
        self.unsubscribed_at = timezone.now()

    def __str__(self):
        return self.user.username
