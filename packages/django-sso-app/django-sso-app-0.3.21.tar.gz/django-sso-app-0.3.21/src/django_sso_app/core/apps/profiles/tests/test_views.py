from django.conf import settings

import json

import jwt
from allauth.account.models import EmailAddress
from allauth.account.adapter import get_adapter
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from ...services.models import Service, Subscription
from django_sso_app.core.utils import get_profile_model

User = get_user_model()
Profile = get_profile_model()


class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        email = self.email = "pippo@disney.com"
        username = self.username = "pippo"
        password = self.password = "paperina"
        updated_password = "pippapippa"


        username2 = "cenerentola"
        email2 = "cenerentola@disney.com"
        password2 = "tanticassi"

        self.user = User.objects.create_user(username=username, email=email, password=password)
        self.user_email = EmailAddress.objects.create(user=self.user,
                                                      email=email,
                                                      primary=True,
                                                      verified=True)

        self.user2 = User.objects.create_user(username=username2, email=email2, password=password2)
        self.user2_email = EmailAddress.objects.create(user=self.user2,
                                                      email=email2,
                                                      primary=True,
                                                      verified=True)

        self.service = Service.objects.create(url='http://example.com')
        self.user_subscription = Subscription.objects.create(user=self.user,
                                                             service=self.service)
        self.service2 = Service.objects.create(url='http://disney.org')

        self.staff_user_username = 'staff'
        self.staff_user_password = 'abc123456'
        self.staff_user = User.objects.create_user(username=self.staff_user_username, email='staff@example.com', password=self.staff_user_password, is_staff=True)
        self.staff_user_email = EmailAddress.objects.create(user=self.staff_user,
                                                      email=self.staff_user.email,
                                                      primary=True,
                                                      verified=True)
        self.staff_user_token = Token.objects.create(user=self.staff_user)

        self.valid_new_profile = {
            'email': 'paperino@gmail.com',
            'username': 'paperino',
            'password': 'nonnapapera',
            'first_name': 'Paolino',
            'referrer': 'http://example.com'
        }

        self.valid_new_profile_hashed_pw = {
            'email': 'paperino@gmail.com',
            'username': 'paperino',
            'password': make_password('nonnapapera'),
            'first_name': 'Paolino',
            'referrer': 'http://example.com'
        }

        self.valid_new_profile_login = {
            'username': 'paperino',
            'password': 'nonnapapera',
            'fingerprint': '123456'
        }


        self.staff_user_valid_login = {
            'username': self.staff_user.username,
            'password': self.staff_user_password,
            'fingerprint': '123456'
        }

        self.valid_login = {
            'username': username,
            'password': password,
            'fingerprint': '123456'
        }

        self.valid_staff_login = {
            'username': 'staff',
            'password': self.staff_user_password,
            'fingerprint': '123456'
        }

        self.valid_unsubscription = {
            'password': password
        }

        self.valid_login_after_password_change = {
            'username': username,
            'password': updated_password,
            'fingerprint': '123456'
        }

        self.valid_profile_update = {
            'first_name': 'Pippo'
        }

        self.valid_password_update = {
            'password': updated_password
        }

        self.valid_email_update = {
            'email': 'pippo2@gmail.com'
        }

        adapter = get_adapter()
        self.device0 = adapter.add_user_device(self.user, '000000')
        self.device1 = adapter.add_user_device(self.user, '111111')

        self.valid_registration = {
            'email': 'topolino@disney.com',
            'username': 'topolino',
            'password1': 'paperina',
            'password2': 'paperina',
            'first_name': 'Mickey',
            'last_name': 'Mouse',
            'country': 'Italia',
            'latitude': 12.345,
            'longitude': 54.321,
            'referrer': 'http://example.com'
        }


class TestProfileRetrieve(ProfileTestCase):

    def test_user_can_retrieve_profile_with_subscriptions(self):
        """
          Registration via rest_auth view
        """
        print('FIRST', json.dumps(self.valid_login))

        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies
        print('RISPSTA1', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.client.get(
            reverse('users:detail', args=(self.user.sso_id, )),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        print('RISPSTA2', response2.data)

        self.assertEqual(response2.data.get('subscriptions'), [{'url': el.service.url, 'is_unsubscribed': el.is_unsubscribed} for el in self.user.subscriptions.all()])



class TestProfileUpdate(ProfileTestCase):

    def test_profile_update_refreshes_and_returns_current_device_jwt_and_deletes_other_devices(self):
        """
        Profile update refreshes caller jwt and deletes all but caller devices
        """
        first_rev = self.user.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies
        print('\n\n\nRESPONSE1!!!!!!\n\n', response.json())

        response2 = self.client.patch(
            '/api/v1/profiles/{0}/'.format(self.user.sso_id),
            data = json.dumps(self.valid_profile_update),
            content_type='application/json'
        )
        cookies2 = response2.cookies

        print('\n\n\nRESPONSE!!!!!!\n\n', response2.json())

        self.user.refresh_from_db()
        second_rev = self.user.sso_rev
        self.assertEqual(second_rev, first_rev+1, 'rev not incremented')

        self.assertTrue(len(cookies2.keys()) > 0, 'no jwt cookie set')

        devices = self.user.devices.all()

        self.assertEqual(devices.count(), 1, 'other devices not deleted')

        self.assertEqual(devices.first().fingerprint, self.valid_login['fingerprint'], 'device not updated')

        jwt_cookie = cookies.get('jwt').value
        jwt_cookie2 = cookies2.get('jwt').value

        # print('\nRISPOSTA, user rev', self.user.sso_rev, '\n\nTOKEN', jwt_cookie)

        unverified_payload = jwt.decode(jwt_cookie, None, False)
        unverified_payload2 = jwt.decode(jwt_cookie2, None, False)

        self.assertEqual(unverified_payload2.get('rev'), unverified_payload.get('rev')+1, 'rev not incremented in cookie')


    def test_profile_update_by_staff_deletes_all_profile_devices(self):
        """
        profile update by staff refreshes deletes all user devices
        """

        first_rev = self.user.sso_rev
        response2 = self.client.patch(
            '/api/v1/profiles/{0}/'.format(self.user.sso_id),
            data = json.dumps(self.valid_profile_update),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.staff_user_token.key)
        )
        cookies2 = response2.cookies

        self.assertTrue(len(cookies2.keys()) == 0, 'jwt cookie set')

        self.user.refresh_from_db()
        second_rev = self.user.sso_rev

        self.assertEqual(second_rev, first_rev+1, 'rev not incremented')

        devices = self.user.devices.all()

        self.assertEqual(devices.count(), 0, 'user devices not deleted')
