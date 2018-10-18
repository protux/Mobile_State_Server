from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Phone
from .utils import signal_utils


@receiver(post_save, sender=Phone, dispatch_uid='post_save_phone')
def post_save_phone(sender, **kwargs):
    phone = kwargs['instance']
    if phone.battery_level is not None:
        if phone.needs_charging:
            signal_utils.initiate_charging(phone)
        else:
            signal_utils.initiate_stop_charging(phone)
