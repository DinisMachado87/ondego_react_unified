from rest_framework import generics, permissions
from ondego_api.permissions import IsOwnerOrReadOnly
from .models import Joining
from .serializers import JoiningSerializer


class JoiningList(generics.ListCreateAPIView):
    serializer_class = JoiningSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        '''
        Returns a list of all the joinings in events by the user and friends
        '''
        user = self.request.user
        friend_ids = user.friend_friends.all().values_list('owner_id', flat=True)
        return Joining.objects.filter(event__owner_id__in=friend_ids)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class JoiningDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JoiningSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        '''
        Returns a list of all the joinings in events by the user and friends
        '''
        user = self.request.user
        friend_ids = user.friend_friends.all().values_list('owner_id', flat=True)
        return Joining.objects.filter(event__owner_id__in=friend_ids)
