from rest_framework import serializers
from .models import Profile
from friends.models import Friend, FriendRequest

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    events_count = serializers.ReadOnlyField()
    joined_events_count = serializers.ReadOnlyField()
    # Friends id is the id of the friend object between the current user and the profile owner
    friends_id = serializers.SerializerMethodField()
    # Has friend request is the id of the friend request from the to-user
    has_friend_request = serializers.SerializerMethodField()
    # Has requested friendship is the id of the friend request from the owner
    has_requested_friendship = serializers.SerializerMethodField()
    friends_count = serializers.ReadOnlyField()
    last_login = serializers.SerializerMethodField()

    def get_friends_id(self, obj):
        '''
        Get the friend object between the current user and the profile owner.
        '''
        user = self.context['request'].user
        if user.is_authenticated:
            # Check if the current user is friend with the profile owner
            friend = Friend.objects.filter(
                owner=user, friend=obj.owner).first()
            return friend.friend.id if friend else None
        return None

    def get_has_friend_request(self, obj):
        '''
        Check if the current user has a friend request from the profile owner.
        '''
        user = self.context['request'].user
        if user.is_authenticated:
            # Check if the current user has a friend request from the profile owner
            friend_request = FriendRequest.objects.filter(
                owner=obj.owner, to_user=user).first()
            return friend_request.to_user.id if friend_request else None
        return None

    def get_has_requested_friendship(self, obj):
        '''
        Check if the current user has requested friendship to the profile owner.
        '''
        user = self.context['request'].user
        if user.is_authenticated:
            # Check if the current user has requested friendship to the profile owner
            friend_request = FriendRequest.objects.filter(
                owner=user, to_user=obj.owner).first()
            return friend_request.owner.id if friend_request else None
        return None

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.owner == request.user

    def get_last_login(self, obj):
        return obj.owner.last_login

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
            'has_friend_request',
            'has_requested_friendship',
            'friends_count',
            'last_login',
        ]
