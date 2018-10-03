from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def number_between_zero_and_one_hundred(value):
    if value < 0 or value > 100:
        raise ValidationError(
            _('Value must be between 0 and 100.')
        )


def positive_number(value):
    if value < 1:
        raise ValidationError(
            _('The value must be positive.')
        )


def positive_or_zero_number(value):
    if value < 0:
        raise ValidationError(
            _('The value must be positive or zero.')
        )
