from django.conf import settings as django_settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from mosta.base import validators
from mosta.power.models import PowerSocket


class Phone(models.Model):
    PHONE_STATE_CALLING = 'calling'
    PHONE_STATE_IDLE = 'idle'
    PHONE_STATE_SWITCHED_OFF = 'switched_off'
    PHONE_STATE_REMOVED = 'removed'
    PHONE_STATE_UNKNOWN = 'unknown'
    PHONE_STATES = (
        (PHONE_STATE_CALLING, _('Calling')),
        (PHONE_STATE_IDLE, _('Idle')),
        (PHONE_STATE_SWITCHED_OFF, _('Switched off')),
        (PHONE_STATE_REMOVED, _('Removed from pool')),
        (PHONE_STATE_UNKNOWN, _('Unknown')),
    )
    owner = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    label = models.CharField(max_length=20)
    battery_level = models.IntegerField(
        blank=True,
        null=True,
        validators=[validators.number_between_zero_and_one_hundred]
    )
    needs_charging = models.BooleanField(default=False)
    state = models.CharField(max_length=15, choices=PHONE_STATES, default=PHONE_STATE_IDLE)
    last_seen = models.DateTimeField(null=True, blank=True)
    attached_power_socket = models.ForeignKey(
        PowerSocket,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.label

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
    balance = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[validators.positive_or_zero_number]
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    can_call = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    class Meta:
        unique_together = (('owner', 'label'),)


class CallHistory(models.Model):
    CALL_DIRECTION_IN = 'in'
    CALL_DIRECTION_OUT = 'out'
    CALL_DIRECTION_UNKNOWN = 'u'
    CALL_DIRECTION_CHOICES = (
        (CALL_DIRECTION_IN, _('Inbound')),
        (CALL_DIRECTION_OUT, _('Outbound')),
        (CALL_DIRECTION_UNKNOWN, _('Unknown')),
    )
    HANGUP_REASON_ABORT = 'abort'
    HANGUP_REASON_CALLEE_HUNG_UP = 'callee_hung_up'
    HANGUP_REASON_CALLER_HUNG_UP = 'caller_hung_up'
    HANGUP_REASON_UNKNOWN = 'unknown'
    HANGUP_REASONS = (
        (HANGUP_REASON_ABORT, _('Aborted')),
        (HANGUP_REASON_CALLEE_HUNG_UP, _('Callee hung up')),
        (HANGUP_REASON_CALLER_HUNG_UP, _('Caller hung up')),
        (HANGUP_REASON_UNKNOWN, _('Unknown'))
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
    ISSUE_TYPE_REQUESTED_CHARGING = 'requested_charging'
    ISSUE_TYPE_ANNOUNCED_CHARGING = 'announced_charging'
    ISSUE_TYPE_ANNOUNCED_FULL_BATTERY = 'announced_full_battery'
    ISSUE_TYPE_STOPPED_CHARGING = 'stopped_charging'
    ISSUE_TYPES = (
        (ISSUE_TYPE_REQUESTED_CHARGING, _('Requested charging')),
        (ISSUE_TYPE_ANNOUNCED_CHARGING, _('Announced charging')),
        (ISSUE_TYPE_ANNOUNCED_FULL_BATTERY, _('Announced full battery')),
        (ISSUE_TYPE_STOPPED_CHARGING, _('Stopped charging')),
    )
    issuer = models.ForeignKey(
        Phone,
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(auto_now_add=True)
    issue_type = models.CharField(max_length=25, choices=ISSUE_TYPES)
    battery_state = models.IntegerField(validators=[validators.number_between_zero_and_one_hundred])


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
    time = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[validators.positive_or_zero_number]
    )
