from rest_framework import generics, permissions
from ondego_api.permissions import IsOwnerOrReadOnly
from .models import Joining
from .serializers import JoiningSerializer


class JoiningList(generics.ListCreateAPIView):
    queryset = Joining.objects.all()
    serializer_class = JoiningSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class JoiningDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Joining.objects.all()
    serializer_class = JoiningSerializer
    permission_classes = [IsOwnerOrReadOnly]
