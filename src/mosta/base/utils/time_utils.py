from datetime import timedelta

from django.utils.translation import ugettext as _
from django.utils import timezone

WEEKDAYS = {
    0: _('Monday'),
    1: _('Tuesday'),
    2: _('Wednesday'),
    3: _('Thursday'),
    4: _('Friday'),
    5: _('Saturday'),
    6: _('Sunday')
}


def get_last_days(days=7):
    now = timezone.now()
    dates = [now]
    for idx in range(1, days):
        dates += [now - timedelta(days=idx)]
    return dates[::-1]


def days_to_weekdays(dates):
    weekdays = []
    for date in dates:
        weekdays += [WEEKDAYS[date.weekday()]]
    return weekdays
