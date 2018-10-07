from django.shortcuts import get_object_or_404
from rest_framework import serializers

from mosta.api.serializers.sim import SimSerializer
from mosta.phone.models import CallHistory, Sim


class CallHistorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    issuer = SimSerializer(read_only=True)

    class Meta:
        model = CallHistory
        fields = (
            'owner',
            'issuer',
            'source_number',
            'destination_number',
            'started',
            'ended',
            'direction',
            'hangup_reason'
        )
        depth = 1


class CallHistoryCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    issuer = SimSerializer()

    def create(self, validated_data):
        sim_label = validated_data.pop('issuer')['label']
        sim = get_object_or_404(Sim, owner=self.context['request'].user, label=sim_label)
        call_history = CallHistory.objects.create(
            owner=self.context['request'].user,
            issuer=sim,
            source_number=validated_data.get('source_number'),
            destination_number=validated_data.get('destination_number'),
            started=validated_data.get('started'),
            ended=validated_data.get('ended'),
            direction=validated_data.get('direction'),
            hangup_reason=validated_data.get('hangup_reason')
        )
        return call_history

    class Meta:
        model = CallHistory
        fields = (
            'owner',
            'issuer',
            'source_number',
            'destination_number',
            'started',
            'ended',
            'direction',
            'hangup_reason'
        )
        depth = 1
