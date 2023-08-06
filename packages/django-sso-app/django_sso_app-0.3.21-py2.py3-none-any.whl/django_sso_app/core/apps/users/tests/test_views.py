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

User = get_user_model()


class UserTestCase(TestCase):
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
            'referrer': 'http://example.com'
        }

        self.valid_new_profile_hashed_pw = {
            'email': 'paperino@gmail.com',
            'username': 'paperino',
            'password': make_password('nonnapapera'),
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


class TestUserRetrieve(UserTestCase):

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

        self.assertEqual(response2.data.get('subscriptions'),
                         [{'url': el.service.url, 'is_unsubscribed': el.is_unsubscribed} for el in self.user.subscriptions.all()])



class TestUserUpdate(UserTestCase):

    def test_user_email_update_deletes_all_devices(self):
        """
        User update refreshes caller jwt and deletes all but caller devices
        """
        print('\n logging in with user', self.user, 'and fingerprint', self.valid_login.get('fingerprint'))
        first_rev = self.user.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        print('\n sending patch from user', self.user, 'with new email', self.valid_email_update)
        response2 = self.client.patch(
            '/api/v1/auth/users/{0}/'.format(self.user.sso_id),
            data = json.dumps(self.valid_email_update),
            content_type='application/json'
        )
        cookies2 = response2.cookies

        self.user.refresh_from_db()
        second_rev = self.user.sso_rev

        self.assertEqual(second_rev, first_rev+1, 'rev not incremented')

        devices = self.user.devices.all()

        self.assertEqual(devices.count(), 0, 'devices not deleted')

    def test_user_password_update_refreshes_and_returns_current_device_jwt_and_deletes_all_devices_but_the_caller(self):
        """
        User password update refreshes caller jwt and deletes all but caller devices
        """

        first_rev = self.user.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies
        self.assertEqual(response.status_code, 200, 'unable to login with valid credentials')

        response2 = self.client.patch(
            '/api/v1/auth/users/{0}/'.format(self.user.sso_id),
            data = json.dumps(self.valid_password_update),
            content_type='application/json'
        )
        cookies2 = response2.cookies

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

        response3 = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login_after_password_change),
            content_type='application/json'
        )
        #print('\n\n\n RISPOSTS!', response3.data)
        cookies3 = response3.cookies

        self.assertEqual(response3.status_code, 200, 'unable to login with new password')
        jwt_cookie3 = cookies3.get('jwt').value
        unverified_payload3 = jwt.decode(jwt_cookie3, None, False)

        print('\n\n\n Unv pay', unverified_payload3)

        self.assertEqual(unverified_payload2.get('rev'), unverified_payload3.get('rev'), 'rev changed after login')

    def test_user_password_update_refreshes_profile_if_called_with_authorization_headers(self):
        """
        User password update
        """

        first_rev = self.user.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        print('RESPONSE1', response.data)
        cookies = response.cookies
        self.assertEqual(response.status_code, 200, 'unable to login with valid credentials')

        received_jwt = cookies.get('jwt').value
        client2 = Client()

        response2 = client2.patch(
            '/api/v1/auth/users/{0}/'.format(self.user.sso_id),
            data = json.dumps(self.valid_password_update),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(received_jwt)
        )

        print('RESPONSE2', self.valid_password_update, response2.data)

        self.assertEqual(response2.status_code, 200, 'cannot patch with jwt inside headers')
        cookies2 = response2.cookies

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

        response3 = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login_after_password_change),
            content_type='application/json'
        )
        #print('\n\n\n RISPOSTS!', response3.data)
        cookies3 = response3.cookies

        self.assertEqual(response3.status_code, 200, 'unable to login with new password')
        jwt_cookie3 = cookies3.get('jwt').value
        unverified_payload3 = jwt.decode(jwt_cookie3, None, False)

        print('\n\n\n Unv pay', unverified_payload3)

        self.assertEqual(unverified_payload2.get('rev'), unverified_payload3.get('rev'), 'rev changed after login')


    def test_user_email_update_by_staff_disables_user_login_user_must_confirm_email(self):
        """
        User update by staff refreshes disables login and deletes all user devices
        """
        first_rev = self.user.sso_rev

        response2 = self.client.patch(
            '/api/v1/auth/users/{0}/'.format(self.user.sso_id),
            data = json.dumps(self.valid_email_update),
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

        self.client.logout()

        response3 = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies3 = response3.cookies

        self.assertEqual(response3.status_code, 400, 'user can login without confirmating email change')

        self.assertEqual(response3.data.get('non_field_errors').pop(), 'E-mail is not verified.')


    def test_user_email_update_by_staff_with_skip_email_confirmation_activates_new_email(self):
        """
        User update by staff refreshes disables login and deletes all user devices
        """
        first_rev = self.user.sso_rev

        print('\n sending patch from user', self.staff_user, 'to user', self.user, 'with new email', self.valid_email_update)
        response2 = self.client.patch(
            '/api/v1/auth/users/{0}/?skip_confirmation=true'.format(self.user.sso_id),
            data = json.dumps(self.valid_email_update),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.staff_user_token.key)
        )
        cookies2 = response2.cookies
        print('Patch response', response2.json())

        self.assertTrue(len(cookies2.keys()) == 0, 'jwt cookie set')

        self.user.refresh_from_db()
        second_rev = self.user.sso_rev

        self.assertEqual(second_rev, first_rev+1, 'rev not incremented')

        devices = self.user.devices.all()

        self.assertEqual(devices.count(), 0, 'user devices not deleted')

        print('\n Trying to login from user', self.user, 'with credentials', self.valid_login)
        response3 = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies3 = response3.cookies

        print('\n Login from user', self.user, 'returns', response3.data)

        self.assertEqual(response3.status_code, 200, 'user can NOT login without confirmating email change')
