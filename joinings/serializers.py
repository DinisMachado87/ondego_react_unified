from django.db import IntegrityError
from rest_framework import serializers
from .models import Joining


class JoiningSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Joining
        fields = [
            'id',
            'owner',
            'event',
            'created_at',
            'updated_at',
            'joining_status',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'You already joined this event.'
            )
