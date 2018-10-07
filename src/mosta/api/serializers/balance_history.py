from django.shortcuts import get_object_or_404
from rest_framework import serializers

from mosta.api.serializers.sim import SimSerializer
from mosta.phone.models import BalanceHistory, Sim


class BalanceHistoryCreateSerializer(serializers.ModelSerializer):
    sim = SimSerializer()

    def create(self, validated_data):
        sim_label = validated_data.pop('sim')['label']
        sim = get_object_or_404(Sim, owner=self.context['request'].user, label=sim_label)
        balance_history = BalanceHistory.objects.create(
            sim=sim,
            time=validated_data.get('time'),
            balance=validated_data.get('balance')
        )
        return balance_history

    class Meta:
        model = BalanceHistory
        fields = (
            'sim',
            'time',
            'balance'
        )
        depth = 1


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
