from rest_framework import serializers
from .models import Profile
from friends.models import Friend



class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    events_count = serializers.ReadOnlyField()
    joined_events_count = serializers.ReadOnlyField()
    friends_id = serializers.SerializerMethodField()
    friends_count = serializers.ReadOnlyField()


    def get_friends_id(self, obj):
        '''
        Get the friend object between the current user and the profile owner.
        '''
        user = self.context['request'].user
        if user.is_authenticated:
            # Check if the current user is friend with the profile owner
            friend = Friend.objects.filter(
                owner=user, friend=obj.owner).first()
            return friend.id if friend else None
        return None


    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.owner == request.user

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'name',
            'feeling',
            'would_like_to',
            'image',
            'is_owner',
            'events_count',
            'joined_events_count',
            'friends_id',
            'friends_count',
        ]
