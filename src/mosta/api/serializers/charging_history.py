from rest_framework import serializers

from mosta.api.serializers.phone import PhoneSerializer
from mosta.phone.models import ChargingHistory


class ChargingHistorySerializer(serializers.ModelSerializer):
    issuer = PhoneSerializer(read_only=True)

    class Meta:
        model = ChargingHistory
        fields = (
            'issuer',
            'time',
            'issue_type',
            'battery_state'
        )
        depth = 1
