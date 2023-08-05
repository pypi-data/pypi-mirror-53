from django.conf import settings
from django.test import TestCase
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

from ...devices.models import Device
from django_sso_app.core.utils import get_profile_model

User = get_user_model()
Profile = get_profile_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="pippo", email="pippo@disney.com")
        self.user_email = EmailAddress.objects.create(user=self.user,
                                                      email=self.user.email,
                                                      primary=True,
                                                      verified=True)
        self.user_device = Device.objects.create(user=self.user,
                                                 fingerprint="abc123",
                                                 apigw_jwt_id="1"
                                                 )

    def test_user_field_update_updates_rev(self):
        """
        User update updates user revision
        """
        user = self.user
        user_rev = user.sso_rev

        user.username = 'pipipipi'
        user.save()

        self.assertEqual(user.sso_rev, user_rev + 1)
