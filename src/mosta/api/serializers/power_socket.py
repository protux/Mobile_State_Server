from rest_framework import serializers

from mosta.power.models import PowerSocket


class PowerSocketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = PowerSocket
        fields = (
            'id',
            'owner',
            'label',
            'namespace',
            'socket_id',
            'active'
        )
        depth = 1
