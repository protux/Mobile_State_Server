from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Phone, Sim, BalanceHistory
from .utils import signal_utils


@receiver(post_save, sender=Phone, dispatch_uid='post_save_phone')
def post_save_phone(sender, **kwargs):
    phone = kwargs['instance']
    if phone.battery_level is not None:
        if phone.needs_charging:
            signal_utils.initiate_charging(phone)
        else:
            signal_utils.initiate_stop_charging(phone)


@receiver(post_save, sender=Sim, dispatch_uid='post_save_sim')
def post_save_sim(sender, **kwargs):
    if not kwargs['created']:
        sim = kwargs['instance']
        latest_balance_history = BalanceHistory.objects.filter(sim=sim).order_by('-time')
        if len(latest_balance_history) > 0:
            latest_balance_history = latest_balance_history[0]

        if not latest_balance_history or latest_balance_history.balance != sim.balance:
            BalanceHistory.objects.create(
                sim=sim,
                balance=sim.balance
            )
