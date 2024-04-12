from rest_framework import generics, permissions
from ondego_api.permissions import IsOwnerOrReadOnly
from .models import Friend, FriendRequest
from .serializers import FriendSerializer, FriendRequestSerializer


class FriendsRequest(generics.ListCreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = FriendRequest.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FriendRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = FriendRequest.objects.all()


class FriendsList(generics.ListCreateAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Friend.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FriendDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Friend.objects.all()
