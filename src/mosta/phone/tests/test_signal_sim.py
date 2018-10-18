import decimal

from django.contrib.auth.models import User
from django.test import TestCase

from mosta.phone.models import Sim, Phone, BalanceHistory


class SimTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test123',
            email='test123@test.tld'
        )
        phone = Phone.objects.create(
            owner=user,
            label='Test_Phone'
        )
        Sim.objects.create(
            owner=user,
            phone=phone,
            label='Test_Sim',
            balance=decimal.Decimal(0),
            phone_number='00001111111',
            can_call=False
        )

    def test_create_adds_no_history(self):
        Sim.objects.create(
            owner=User.objects.get(),
            phone=Phone.objects.get(),
            label='Created_Sim',
            balance=decimal.Decimal(0),
            phone_number='11110000000',
            can_call=False
        )
        self.assertEqual(0, len(BalanceHistory.objects.all()))

    def test_add_history_to_empty_history(self):
        sim = Sim.objects.get()
        sim.balance = decimal.Decimal(5)
        sim.save()
        balance_history = BalanceHistory.objects.all()
        self.assertEqual(1, len(balance_history))
        self.assertEqual(decimal.Decimal(5), balance_history[0].balance)
        self.assertEqual(sim, balance_history[0].sim)

    def test_add_second_history_entry(self):
        sim = Sim.objects.get()
        sim.balance = decimal.Decimal(5)
        sim.save()
        sim.balance = decimal.Decimal(6.5)
        sim.save()
        balance_history = BalanceHistory.objects.all().order_by('time')
        self.assertEqual(2, len(balance_history))

        self.assertEqual(decimal.Decimal(5), balance_history[0].balance)
        self.assertEqual(sim, balance_history[0].sim)

        self.assertEqual(decimal.Decimal(6.5), balance_history[1].balance)
        self.assertEqual(sim, balance_history[1].sim)

    def test_add_same_history_entry_twice(self):
        sim = Sim.objects.get()
        sim.balance = decimal.Decimal(5)
        sim.save()
        sim.save()
        balance_history = BalanceHistory.objects.all()
        self.assertEqual(1, len(balance_history))
        self.assertEqual(decimal.Decimal(5), balance_history[0].balance)
        self.assertEqual(sim, balance_history[0].sim)
