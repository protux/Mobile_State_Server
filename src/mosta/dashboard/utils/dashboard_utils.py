from datetime import datetime, timedelta

from django.utils.translation import ugettext as _

from mosta.phone.models import Phone, SMS, BalanceHistory


def get_missing_phones(user):
    missing_phones = Phone.objects.filter(owner=user, last_seen__lt=datetime.now() - timedelta(days=2))
    if len(missing_phones) > 0:
        return missing_phones


def get_latest_sms(user):
    sms = SMS.objects.filter(owner=user).order_by('-time_received')[:10]
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
