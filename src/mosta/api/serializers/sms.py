from django.shortcuts import get_object_or_404
from rest_framework import serializers

from mosta.api.serializers.sim import SimSerializer
from mosta.phone.models import SMS, Sim


class SMSCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    sim = SimSerializer()

    def create(self, validated_data):
        sim_label = validated_data.pop('sim')['label']
        sim = get_object_or_404(Sim, owner=self.context['request'].user, label=sim_label)
        sms = SMS.objects.create(
            owner=self.context['request'].user,
            sim=sim,
            sender=validated_data.get('sender'),
            content=validated_data.get('content'),
            time_received=validated_data.get('time_received')
        )
        return sms

    class Meta:
        model = SMS
        fields = (
            'owner',
            'sim',
            'sender',
            'content',
            'time_received'
        )
        depth = 1


class SMSSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    sim = SimSerializer(read_only=True)

    class Meta:
        model = SMS
        fields = (
            'owner',
            'sim',
            'sender',
            'content',
            'time_received'
        )
        depth = 1
