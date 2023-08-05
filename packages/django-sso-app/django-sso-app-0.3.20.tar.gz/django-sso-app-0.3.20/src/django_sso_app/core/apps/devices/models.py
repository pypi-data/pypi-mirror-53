import logging

from django.db import models
from django.contrib.auth import get_user_model

from ...models import CreatedAtModel

logger = logging.getLogger('devices')
User = get_user_model()


class Device(CreatedAtModel):
    # deleting deletes jwt by delete_device_jwt signal!

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="devices"
    )

    fingerprint = models.CharField(max_length=32)
    user_agent = models.CharField(max_length=32, null=True, blank=True)

    apigw_jwt_id = models.CharField(max_length=36, null=True, blank=True)
    apigw_jwt_key = models.CharField(max_length=32, null=True, blank=True)
    apigw_jwt_secret = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
      return '{}:{}'.format(self.id, self.fingerprint)
