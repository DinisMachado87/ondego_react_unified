from django.db import models
from django.db import IntegrityError
from rest_framework import serializers
from .models import Friend, FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    '''
    Serializer for the FriendRequest model.
    Intermidiate model to create a friend instance between two users.
    '''
    owner = serializers.ReadOnlyField(source='owner.id')
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = FriendRequest
        fields = [
            'id',
            'owner',
            'to_user',
            'is_approved',
            'created_at',
        ]

    def create(self, validated_data):
        '''
        Create a new friend request instance
        '''
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'Friend already requested'
            })


class FriendSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Friend model
    '''
    owner = serializers.ReadOnlyField(source='owner.id')
    friend = serializers.ReadOnlyField(source='friend.id')
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Friend
        fields = [
            'id',
            'owner',
            'friend',
            'created_at',
        ]
