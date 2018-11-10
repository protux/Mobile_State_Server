from rest_framework import serializers

from mosta.phone.models import PowerSocket


class PowerSocketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

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
