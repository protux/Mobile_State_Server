from django.shortcuts import get_object_or_404
from rest_framework import serializers

from mosta.api.serializers.phone import PhoneSerializer
from mosta.phone.models import ChargingHistory, Phone


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


class ChargingCreateHistorySerializer(serializers.ModelSerializer):
    issuer = PhoneSerializer()

    def create(self, validated_data):
        phone_label = validated_data.pop('issuer')['label']
        phone = get_object_or_404(Phone, owner=self.context['request'].user, label=phone_label)
        charging_history = ChargingHistory.objects.create(
            issuer=phone,
            time=validated_data.get('time'),
            issue_type=validated_data.get('issue_type'),
            battery_state=validated_data.get('battery_state')
        )
        return charging_history

    class Meta:
        model = ChargingHistory
        fields = (
            'issuer',
            'time',
            'issue_type',
            'battery_state'
        )
        depth = 1
