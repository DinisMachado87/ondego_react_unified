from rest_framework import generics, permissions
from ondego_api.permissions import (
    IsOwnerOrReadOnly,
    IsFriendRequestedOrReadOnly,
    IsFriendOwnerToDelete
)
from django.http import Http404
from .models import Friend, FriendRequest
from .serializers import FriendSerializer, FriendRequestSerializer


class FriendsRequest(generics.ListCreateAPIView):
    '''
    List all friend requests for a user
    '''
    serializer_class = FriendRequestSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = FriendRequest.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FriendRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete a friend request
    '''
    serializer_class = FriendRequestSerializer
    permission_classes = [IsFriendRequestedOrReadOnly]
    queryset = FriendRequest.objects.all()


class FriendsList(generics.ListAPIView):
    '''
    List all friends for a user
    '''
    serializer_class = FriendSerializer
    permission_classes = [IsFriendOwnerToDelete]

    def get_queryset(self):
        """
        Returns a list of all the friends
        for the currently authenticated user, 
        or an empty list if the user is not authenticated.
        """
        user = self.request.user
        if user.is_authenticated:
            return Friend.objects.filter(owner=user)
        else:
            return Friend.objects.none()


class FriendDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete a friend
    '''
    serializer_class = FriendSerializer
    permission_classes = [IsFriendOwnerToDelete]
    queryset = Friend.objects.all()
