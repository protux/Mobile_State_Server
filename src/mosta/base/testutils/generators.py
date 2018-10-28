import random
import string
from datetime import datetime, timedelta
from decimal import Decimal

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.utils import timezone

from mosta.phone.models import Phone, Sim, CallHistory

CHARSET = string.ascii_letters + string.digits


def get_random_string(charset=CHARSET, length=20):
    return ''.join(random.choices(charset, k=length))


def get_random_mail_address(charset=CHARSET, length=20):
    return ''.join(
        (
            get_random_string(charset, int(length / 2)),
            '@',
            get_random_string(charset, int(length / 2)),
        )
    )[:length]


def generate_test_user(validate_email_address=True):
    user = User.objects.create(
        username=get_random_string(),
        email=get_random_mail_address()
    )

    if validate_email_address:
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            verified=True,
            primary=True
        )

    return user


def generate_phone(owner, power_socket=None):
    return Phone.objects.create(
        owner=owner,
        label=get_random_string(length=5),
        battery_level=50,
        needs_charging=False,
        last_seen=timezone.now(),
        attached_power_socket=power_socket
    )


def generate_sim(owner, phone, can_call=False):
    return Sim.objects.create(
        owner=owner,
        phone=phone,
        label=get_random_string(length=5),
        balance=Decimal(15),
        phone_number=get_random_string(charset=string.digits, length=11),
        can_call=can_call
    )


def generate_calling_history(owner, sim, date, entry_count, call_durations=None):
    call_history = []

    if call_durations and len(call_durations) != entry_count:
        raise Exception(
            'len(call_durations) must be equal to {}, but was {}.'.format(entry_count, len(call_durations))
        )

    if not call_durations:
        call_durations = []
        for idx in range(entry_count):
            call_durations += [int(random.random() * 40)]

    source_number = sim.phone_number if sim.can_call else get_random_string(charset=string.digits, length=11)
    destination_number = get_random_string(charset=string.digits, length=11) if sim.can_call else sim.phone_number

    for idx in range(0, entry_count):
        start_time = __generate_started_time(date)

        call_history += [CallHistory.objects.create(
            owner=owner,
            issuer=sim,
            source_number=source_number,
            destination_number=destination_number,
            started=start_time,
            ended=__add_call_duration(start_time, call_durations.pop(0)),
            direction=CallHistory.CALL_DIRECTION_OUT if sim.can_call else CallHistory.CALL_DIRECTION_IN
        )]

    return call_history


def __generate_started_time(date: datetime):
    hour = int(random.random() * 23)
    minute = int(random.random() * 60)
    return date.replace(hour=hour, minute=minute)


def __add_call_duration(date, duration):
    return date + timedelta(minutes=duration)
