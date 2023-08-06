import logging
import uuid

from django.contrib.auth.hashers import identify_hasher, get_hasher
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

logger = logging.getLogger('users')


class AbstractUserModel(AbstractUser):
    """
    Abstract user model, the fields below should be defined by 'django.contrib.auth.models.AbstractUser'

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    """

    class Meta:
        abstract = True

    # set unique=False on first migration to enable model swap
    sso_id = models.UUIDField(_('sso id'), unique=True, db_index=True, default=uuid.uuid4, editable=False)
    sso_rev = models.PositiveIntegerField(_('sso revision'), default=1)

    unsubscribed_at = models.DateTimeField(_('unsubscription date'), null=True, blank=True)
    apigw_consumer_id = models.CharField(_('apigw consumer id'), max_length=36, null=True, blank=True)

    @property
    def created_at(self):
        return self.date_joined

    @property
    def is_unsubscribed(self):
        return self.unsubscribed_at is not None

    @is_unsubscribed.setter
    def is_unsubscribed(self, value):
        self.unsubscribed_at = timezone.now()

    def set_password(self, raw_password):
        setattr(self, '__password_updated', True)
        return super(AbstractUserModel, self).set_password(raw_password)

    def __str__(self):
        return '{}:{}'.format(self.username, self.id)

    def serialized_as_string(self):
        serialized = ''
        for f in settings.DJANGO_SSO_USER_FIELDS + ('password',):
            field = getattr(self, f, None)
            if f == 'password':
                pass
                """
                if field and len(field):
                    print('PASS', f, field)
                    (algorithm, iterations, salt, hash) = field.split('$')
                    print('PASS', (algorithm, iterations, salt, hash))
                    serialized += hash
                else:
                    serialized += str(field)
                """
            else:
                serialized += str(field)


        # logger.debug('serialized_as_string {}'.format(serialized))
        return serialized

    def __init__(self, *args, **kwargs):
        super(AbstractUserModel, self).__init__(*args, **kwargs)
        setattr(self, '__serialized_as_string', self.serialized_as_string())

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.first_name:
                self.first_name = ''
            if not self.last_name:
                self.last_name = ''
        return super(AbstractUserModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("users:detail", args=[self.sso_id])

    def check_password(self, raw_password):
        # password is hashed, checking if will be runtime hardened
        # taken from django.contrib.auth.hashers.check_password
        old_hashed_password = self.password

        preferred = get_hasher('default')

        try:
            hasher = identify_hasher(old_hashed_password)
        except ValueError:
            hasher = None

        if hasher is not None:
            hasher_changed = hasher.algorithm != preferred.algorithm
            if hasher_changed:
                logger.info(
                    '!!! Password hasher for {} changed from {} to {}'.format(self,
                                                                              hasher.algorithm,
                                                                              preferred.algorithm))
            must_update = hasher_changed or hasher.must_update(old_hashed_password)
            if must_update:
                setattr(self, '__password_hardened', True)

        return super(AbstractUserModel, self).check_password(raw_password)

    def update_rev(self, commit=False):
        logger.info('Updating rev for User {0}, commit? {1}'.format(self, commit))
        self.sso_rev = F('sso_rev') + 1
        if commit:
            self.save()
            self.refresh_from_db()

    def unsubscribe(self):
        logger.info('Unsubscribing User {0}'.format(self))
        try:
            with transaction.atomic():
                self.unsubscribed_at = timezone.now()
                self.is_active = False
                self.update_rev(True)

        except Exception as e:
            logger.error(
                'Unsubscription error {0} for User {1}'.format(e, self),
                exc_info=True)
