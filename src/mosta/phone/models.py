from django.conf import settings as django_settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from mosta.power.models import PowerSocket


class Phone(models.Model):
    PHONE_STATES = (
        ('calling', _('Calling')),
        ('idle', _('Idle')),
        ('switched_off', _('Switched off')),
        ('removed', _('Removed from pool')),
        ('unknown', _('Unknown')),
    )
    owner = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    label = models.CharField(max_length=20)
    battery_level = models.IntegerField(blank=True, null=True)
    needs_charging = models.BooleanField(default=False)
    state = models.CharField(max_length=15, choices=PHONE_STATES)
    last_seen = models.DateTimeField()
    attached_power_socket = models.ForeignKey(
        PowerSocket,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = (('owner', 'label'),)


class Sim(models.Model):
    owner = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phone = models.ForeignKey(
        Phone,
        on_delete=models.CASCADE
    )
    label = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    can_call = models.BooleanField(default=False)

    class Meta:
        unique_together = (('owner', 'label'),)


class CallHistory(models.Model):
    CALL_DIRECTION_CHOICES = (
        ('in', _('Inbound')),
        ('out', _('Outbound')),
        ('u', _('Unknown')),
    )
    HANGUP_REASONS = (
        ('abort', _('Aborted')),
        ('callee_hung_up', _('Callee hung up')),
        ('caller_hung_up', _('Caller hung up')),
        ('unknown', _('Unknown'))
    )
    owner = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    issuer = models.ForeignKey(
        Sim,
        on_delete=models.CASCADE
    )
    source_number = models.CharField(max_length=20)
    destination_number = models.CharField(max_length=20)
    started = models.DateTimeField()
    ended = models.DateTimeField()
    direction = models.CharField(max_length=3, choices=CALL_DIRECTION_CHOICES)
    hangup_reason = models.CharField(max_length=15, choices=HANGUP_REASONS)


class ChargingHistory(models.Model):
    ISSUE_TYPES = (
        ('requested_charging', _('Requested charging')),
        ('announced_charging', _('Announced charging')),
        ('announced_full_battery', _('Announced full battery')),
        ('stopped_charging', _('Stopped charging')),
    )
    issuer = models.ForeignKey(
        Phone,
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(auto_now_add=True)
    issue_type = models.CharField(max_length=25, choices=ISSUE_TYPES)
    battery_state = models.IntegerField()


class SMS(models.Model):
    owner = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    sim = models.ForeignKey(
        Sim,
        on_delete=models.CASCADE
    )
    sender = models.CharField(max_length=20)
    content = models.CharField(max_length=160)
    time_received = models.DateTimeField()


class BalanceHistory(models.Model):
    sim = models.ForeignKey(
        Sim,
        on_delete=models.CASCADE
    )
    time = models.DateTimeField()
    balance = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
