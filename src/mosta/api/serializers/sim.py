from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.utils import model_meta

from mosta.phone.models import Phone, Sim
from .phone import PhoneSerializer


class SimSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    phone = PhoneSerializer()

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            elif attr is not 'phone':
                setattr(instance, attr, value)

        related_label = validated_data['phone']['label']
        related_phone = get_object_or_404(Phone, owner=instance.owner, label=related_label)
        instance.phone = related_phone
        instance.save()

        return instance

    class Meta:
        model = Sim
        fields = (
            'owner',
            'phone',
            'label',
            'balance',
            'phone_number',
            'can_call'
        )
        depth = 1
