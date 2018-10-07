from django.contrib.sessions.models import Session
from django import template

from mosta.base.utils import message_utils

register = template.Library()


@register.simple_tag
def get_error_messages(session: Session):
    return message_utils.get_error_messages(session)


@register.simple_tag
def get_success_messages(session: Session):
    return message_utils.get_success_messages(session)
