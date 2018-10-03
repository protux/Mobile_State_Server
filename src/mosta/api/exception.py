from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def rest_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
    elif 'UNIQUE constraint failed' in str(exc):
        response = Response(
            {'detail': _('A phone with this label is already registered for this user.')},
            status.HTTP_409_CONFLICT
        )

    return response
