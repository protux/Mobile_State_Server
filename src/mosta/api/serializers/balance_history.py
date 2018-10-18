from rest_framework import serializers

from mosta.phone.models import BalanceHistory


class BalanceHistorySerializer(serializers.ModelSerializer):
    sim = serializers.ReadOnlyField(source='sim.label')

    class Meta:
        model = BalanceHistory
        fields = (
            'sim',
            'time',
            'balance'
        )
        depth = 1
