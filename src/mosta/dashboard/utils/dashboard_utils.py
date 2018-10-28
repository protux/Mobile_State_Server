import json
from datetime import timedelta
from decimal import Decimal

from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext as _

from mosta.base.utils import time_utils
from mosta.base import json_encoders
from mosta.phone.models import Phone, SMS, BalanceHistory, CallHistory, Sim


def get_missing_phones(user):
    missing_phones = Phone.objects.filter(owner=user, last_seen__lt=timezone.now() - timedelta(days=2))
    if len(missing_phones) > 0:
        return missing_phones


def get_latest_sms(user, sms_count=10):
    sms = SMS.objects.filter(owner=user).order_by('-time_received')[:sms_count]
    if len(sms) > 0:
        return sms


def get_latest_balance_changes(user):
    latest_balances = BalanceHistory.objects.filter(sim__owner=user).order_by('-time')[:10]
    latest_balance_changes = []

    for latest_balance in latest_balances:
        latest_changes = BalanceHistory.objects.filter(sim=latest_balance.sim).order_by('-time')[:2]
        if len(latest_changes) == 2:
            latest_balance_changes += [(
                latest_balance, round(latest_balance.balance - latest_changes[1].balance, 2)
            )]
        else:
            latest_balance_changes += [(
                latest_balance, '({})'.format(_('new'))
            )]

    if len(latest_balance_changes) > 0:
        return latest_balance_changes


def get_average_call_duration(user, date, sim=None):
    """
    :param user: the owner of the call history
    :param date: the date to calculate the duration for
    :param sim: if set only calls by this sim are looked at
    :return: the average call duration in seconds
    """
    call_history = CallHistory.objects.filter(
        owner=user,
        ended__year=date.year,
        ended__month=date.month,
        ended__day=date.day
    )
    if sim:
        call_history = call_history.filter(issuer=sim)

    if len(call_history) == 0:
        return 0

    duration = timedelta()
    for call in call_history:
        duration += call.ended - call.started
    return duration.total_seconds() / len(call_history)


def get_sim_cards_divergent_from_average_call_duration(user, max_divergence_in_minutes, date):
    """
    :param user the owner of the calling sims
    :param max_divergence_in_minutes:
    :param date: the date of the calls to look at
    :return: a list of all divergent phones or an empty list
    """
    max_divergence_in_seconds = max_divergence_in_minutes * 0
    call_history = CallHistory.objects.filter(
        owner=user,
        ended__year=date.year,
        ended__month=date.month,
        ended__day=date.day
    ).prefetch_related()
    average_call_duration = get_average_call_duration(user, date)
    checked_sims = []
    divergent_sims = []

    for call in call_history:
        if call.issuer not in checked_sims:
            average_call_duration_per_sim = get_average_call_duration(user, date, sim=call.issuer)
            average_call_duration_divergence = average_call_duration_per_sim - average_call_duration
            average_call_duration_divergence = max(average_call_duration_divergence,
                                                   average_call_duration_divergence * -1)
            if average_call_duration_divergence > max_divergence_in_seconds:
                divergent_sims += [{'sim': call.issuer, 'divergence': average_call_duration_divergence}]
        checked_sims += [call.issuer]

    return divergent_sims


def get_phones_requiring_energy(user):
    return Phone.objects.filter(
        Q(owner=user),
        Q(needs_charging=True),
        Q(attached_power_socket__isnull=True) | Q(attached_power_socket__active=False)
    )


def get_phones_charging(user):
    return Phone.objects.filter(
        owner=user,
        attached_power_socket__active=True
    )


def get_call_duration_over_time_per_sim(user, days=7):
    sims = Sim.objects.filter(owner=user)
    dates = time_utils.get_last_days(days)
    data_sets = []
    for sim in sims:
        data = []
        for date in dates:
            call_history = CallHistory.objects.filter(
                owner=user,
                issuer=sim,
                started__day=date.day,
                started__month=date.month,
                started__year=date.year
            )
            call_duration = 0
            for call in call_history:
                call_duration += (call.ended - call.started).seconds
            data += [int(call_duration / 60)]
        data_sets += [{
            'label': sim.label,
            'data': data
        }]
    weekdays = time_utils.days_to_weekdays(dates)
    return {'datasets': json.dumps(data_sets), 'labels': json.dumps(weekdays)}


def get_balance_over_time_per_sim(user, days=7):
    sims = Sim.objects.filter(owner=user)
    dates = time_utils.get_last_days(days)
    data_sets = []
    for sim in sims:
        data = []
        for date in dates:
            balance_history = BalanceHistory.objects.filter(
                sim=sim,
                time__day=date.day,
                time__month=date.month,
                time__year=date.year
            ).order_by('-time')[:1]
            if len(balance_history) == 0:
                if len(data) > 0:
                    data += [data[-1]]
                else:
                    data += [Decimal(0)]
            else:
                data += [balance_history[0].balance]
        data_sets += [{
            'label': sim.label,
            'data': data
        }]
    weekdays = time_utils.days_to_weekdays(dates)
    return {'datasets': json.dumps(data_sets, cls=json_encoders.DecimalEncoder), 'labels': json.dumps(weekdays)}
