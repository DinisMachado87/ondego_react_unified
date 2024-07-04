from rest_framework import generics, permissions
from ondego_api.permissions import IsOwnerOrReadOnly
from .models import Joining
from .serializers import JoiningSerializer


class JoiningList(generics.ListCreateAPIView):
    def get_queryset(self):
        """
        Returns a list of all the joinings by all users 
        but only to events where the owner is Friend of the user
        """
        user = self.request.user
        return Joining.objects.filter(event__owner__friend__friend=user)
    serializer_class = JoiningSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class JoiningDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JoiningSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        """
        Returns a list of all the joinings by all users 
        but only to events where the owner is Friend of the user
        """
        user = self.request.user
        return Joining.objects.filter(event__owner__friend__friend=user)
