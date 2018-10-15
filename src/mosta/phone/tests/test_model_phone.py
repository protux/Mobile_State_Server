from django.contrib.auth.models import User
from django.test import TestCase

from mosta.phone.models import Phone, ChargingHistory
from mosta.power.models import PowerSocket


class PhoneTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test123',
            email='test123@test.tld'
        )
        PowerSocket.objects.create(
            owner=user,
            label='Test Socket',
            namespace='10001',
            socket_id=4
        )

    def test_phone_add_phone_without_socket(self):
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE'
        )
        phone = Phone.objects.get()
        self.assertFalse(phone.needs_charging)
        charging_history_count = ChargingHistory.objects.filter(issuer=phone).count()
        self.assertEqual(0, charging_history_count)

    def test_phone_add_phone_with_socket(self):
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE',
            attached_power_socket=PowerSocket.objects.get()
        )
        phone = Phone.objects.get()
        power_socket = PowerSocket.objects.get()
        self.assertFalse(phone.needs_charging)
        self.assertFalse(power_socket.active)
        charging_history_count = ChargingHistory.objects.filter(issuer=phone).count()
        self.assertEqual(0, charging_history_count)

    def test_phone_add_phone_needs_charging(self):
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE',
            attached_power_socket=PowerSocket.objects.get(),
            needs_charging=True,
            battery_level=15
        )
        phone = Phone.objects.get()
        power_socket = PowerSocket.objects.get()
        self.assertTrue(power_socket.active)
        charging_history = ChargingHistory.objects.filter(issuer=phone)
        self.assertEqual(1, len(charging_history))
        self.assertEqual(ChargingHistory.ISSUE_TYPE_REQUESTED_CHARGING, charging_history[0].issue_type)

    def test_phone_add_phone_needs_charging_no_socket(self):
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE',
            needs_charging=True,
            battery_level=15
        )
        phone = Phone.objects.get()
        charging_history = ChargingHistory.objects.filter(issuer=phone)
        self.assertEqual(1, len(charging_history))
        self.assertEqual(ChargingHistory.ISSUE_TYPE_REQUESTED_CHARGING, charging_history[0].issue_type)

    def test_phone_add_phone_needs_charging_socket_already_active(self):
        power_socket = PowerSocket.objects.create(
            owner=User.objects.get(),
            label='Test Socket2',
            namespace='10011',
            socket_id=1,
            active=True
        )
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE',
            attached_power_socket=power_socket,
            needs_charging=True,
            battery_level=15
        )
        phone = Phone.objects.get()
        power_socket = PowerSocket.objects.get(pk=power_socket.id)
        self.assertTrue(power_socket.active)
        charging_history = ChargingHistory.objects.filter(issuer=phone)
        self.assertEqual(1, len(charging_history))
        self.assertEqual(ChargingHistory.ISSUE_TYPE_ANNOUNCED_CHARGING, charging_history[0].issue_type)

    def test_phone_add_phone_needs_charging_socket_duplicate_save(self):
        power_socket = PowerSocket.objects.get()
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE',
            attached_power_socket=power_socket,
            needs_charging=True,
            battery_level=15
        )
        phone = Phone.objects.get()
        phone.label = 'CHANGED'
        phone.save()
        power_socket = PowerSocket.objects.get(pk=power_socket.id)
        self.assertTrue(power_socket.active)
        charging_history = ChargingHistory.objects.filter(issuer=phone)
        self.assertEqual(1, len(charging_history))
        self.assertEqual(ChargingHistory.ISSUE_TYPE_REQUESTED_CHARGING, charging_history[0].issue_type)

    def test_phone_no_charging_only_phone(self):
        power_socket = PowerSocket.objects.create(
            owner=User.objects.get(),
            label='SOCKET',
            namespace='11111',
            socket_id=5,
            active=True
        )
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE',
            attached_power_socket=power_socket,
            needs_charging=False,
            battery_level=15
        )
        power_socket = PowerSocket.objects.get(pk=power_socket.id)
        self.assertFalse(power_socket.active)

    def test_phone_no_charging_other_phones_still_loading(self):
        power_socket = PowerSocket.objects.create(
            owner=User.objects.get(),
            label='SOCKET',
            namespace='11111',
            socket_id=5,
            active=True
        )
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE2',
            attached_power_socket=power_socket,
            needs_charging=True,
            battery_level=15
        )
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE',
            attached_power_socket=power_socket,
            needs_charging=False,
            battery_level=15
        )
        power_socket = PowerSocket.objects.get(pk=power_socket.id)
        self.assertTrue(power_socket.active)

    def test_phone_no_charging_another_fully_charged_phone(self):
        power_socket = PowerSocket.objects.create(
            owner=User.objects.get(),
            label='SOCKET',
            namespace='11111',
            socket_id=5,
            active=True
        )
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE2',
            attached_power_socket=power_socket,
            needs_charging=False,
            battery_level=15
        )
        power_socket.active = True
        power_socket.save()
        Phone.objects.create(
            owner=User.objects.get(),
            label='TESTPHONE',
            attached_power_socket=power_socket,
            needs_charging=False,
            battery_level=15
        )
        power_socket = PowerSocket.objects.get(pk=power_socket.id)
        self.assertFalse(power_socket.active)

    def test_phone_no_charging_no_socket(self):
        try:
            Phone.objects.create(
                owner=User.objects.get(),
                label='TESTPHONE',
                needs_charging=False,
                battery_level=15
            )
        except Exception as e:
            self.fail('No Exception expected', e)
