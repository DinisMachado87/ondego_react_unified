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
        '''
        Create a new joining instance
        if the user has not already joined the event.
        '''
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'You already made this choice.'
            )
