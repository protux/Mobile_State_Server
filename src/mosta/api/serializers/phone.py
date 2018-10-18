from rest_framework import serializers

from mosta.phone.models import Phone, PowerSocket


class PhoneSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    attached_power_socket = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=PowerSocket.objects.all())

    class Meta:
        model = Phone
        fields = (
            'id',
            'owner',
            'label',
            'battery_level',
            'needs_charging',
            'state',
            'last_seen',
            'attached_power_socket'
        )
        depth = 1
