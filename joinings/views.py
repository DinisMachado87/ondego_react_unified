from rest_framework import generics, permissions
from ondego_api.permissions import IsFriendOfEventOwnerToSeeAndOwnerToEditOrDelete
from .models import Joining
from .serializers import JoiningSerializer


class JoiningList(generics.ListCreateAPIView):
    queryset = Joining.objects.all()
    serializer_class = JoiningSerializer
    permission_classes = [IsFriendOfEventOwnerToSeeAndOwnerToEditOrDelete]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class JoiningDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JoiningSerializer
    permission_classes = [IsFriendOfEventOwnerToSeeAndOwnerToEditOrDelete]
    queryset = Joining.objects.all()
