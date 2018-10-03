from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def number_between_zero_and_one_hundred(value):
    if value < 0 or value > 100:
        raise ValidationError(
            _('Value must be between 0 and 100.')
        )
