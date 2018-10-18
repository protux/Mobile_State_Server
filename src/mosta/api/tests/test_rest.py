from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from mosta.phone.models import Phone, PowerSocket
from mosta.utils import test_utils


class TestPhone(APITestCase):
    PHONE = {
        'owner': None,
        'label': None,
        'battery_level': 100,
        'needs_charging': False,
        'state': 'idle',
        'last_seen': timezone.now(),
        'attached_power_socket': None,
    }

    @classmethod
    def setUpTestData(cls):
        test_utils.create_random_user()

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(user=self.user)
        self.phone = dict(TestPhone.PHONE)
        self.phone.update({
            'owner': self.user.id,
            'label': test_utils.get_random_string(),
        })

    def test_create_phone(self):
        response = self.client.post(reverse('phone-list'), self.phone)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Phone.objects.count(), 1)
        db_phone = Phone.objects.get()
        self.assertEqual(db_phone.owner, self.user)
        self.assertEqual(db_phone.label, self.phone['label'])
        self.assertEqual(db_phone.battery_level, self.phone['battery_level'])
        self.assertEqual(db_phone.needs_charging, self.phone['needs_charging'])
        self.assertEqual(db_phone.state, self.phone['state'])
        self.assertEqual(db_phone.last_seen, self.phone['last_seen'])
        self.assertEqual(db_phone.attached_power_socket, self.phone['attached_power_socket'])

    def test_update_phone(self):
        self.client.post(reverse('phone-list'), self.phone)
        db_phone = Phone.objects.get()
        self.assertEqual(db_phone.battery_level, 100)
        self.phone['battery_level'] = 50
        self.client.put(reverse('phone-detail', args=[db_phone.id]), self.phone)
        updated_phone = Phone.objects.get()
        self.assertEqual(updated_phone.battery_level, 50)

    def test_add_same_phone_twice(self):
        self.client.post(reverse('phone-list'), self.phone)
        response = self.client.post(reverse('phone-list'), self.phone)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_get_phone_by_owner(self):
        self.client.post(reverse('phone-list'), self.phone)
        response = self.client.get(reverse('phone-list'))
        phone = Phone.objects.get()
        self.assertEqual(len(response.data), 1)
        rest_phone = response.data[0]
        self.assertEqual(rest_phone['owner'], phone.owner.email)
        self.assertEqual(rest_phone['id'], phone.id)

    def test_get_phone_list(self):
        """
        Tests, if a user gets only their own phones.
        """
        self.client.post(reverse('phone-list'), self.phone)

        second_user = test_utils.create_random_user()
        self.client.force_login(second_user)
        second_phone = dict(TestPhone.PHONE)
        second_phone.update({
            'owner': second_user.id,
            'label': test_utils.get_random_string()
        })
        self.client.post(reverse('phone-list'), second_phone)

        response = self.client.get(reverse('phone-list'))
        phone = Phone.objects.get(pk=2)
        self.assertEqual(len(response.data), 1)
        rest_phone = response.data[0]
        self.assertEqual(rest_phone['owner'], phone.owner.email)
        self.assertEqual(rest_phone['id'], phone.id)

    def test_get_phone_non_owner(self):
        """
        check if user gets error if they try to fetch foreign phone
        """
        self.client.post(reverse('phone-list'), self.phone)
        self.client.logout()
        response = self.client.get(reverse('phone-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_phone_non_owner(self):
        """
        check if user gets error if they try to update foreign phone
        """
        self.client.post(reverse('phone-list'), self.phone)
        self.client.logout()

        second_user = test_utils.create_random_user()
        self.client.force_login(second_user)
        updated_phone = dict(self.phone)
        updated_phone.update({
            'label': test_utils.get_random_string(),
        })
        response = self.client.put(reverse('phone-detail', args=[1]), updated_phone)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_power_socket(self):
        """
        check if power socket is changeable
        """
        self.client.post(reverse('phone-list'), self.phone)
        power_socket = PowerSocket.objects.create(
            owner=self.user,
            label=test_utils.get_random_string(),
            namespace='10001',
            socket_id=4
        )
        phone = dict(self.phone)
        phone.update({
            'attached_power_socket': power_socket.id,
        })
        response = self.client.put(reverse('phone-detail', args=[1]), phone)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['attached_power_socket'], 1)
