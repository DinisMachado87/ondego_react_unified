from rest_framework import generics, permissions
from ondego_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializer import CommentSerializer, CommentDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CommentList(generics.ListCreateAPIView):
    def get_queryset(self):
        """
        Returns a list of all the comments by all users 
        but only to events where the owner is Friend of the user
        """
        user = self.request.user
        return Comment.objects.filter(event__owner__friend__friend=user)
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        """
        Returns a list of all the comments by all users 
        but only to events where the owner is Friend of the user
        """
        user = self.request.user
        return Comment.objects.filter(event__owner__friend__friend=user)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']
