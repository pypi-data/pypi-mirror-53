import logging

from django.contrib.auth.models import Group as GroupModel
from django.urls import reverse

logger = logging.getLogger('groups')


class Group(GroupModel):
    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse("group:detail", args=[self.pk])
