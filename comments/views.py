from rest_framework import generics, permissions
from ondego_api.permissions import IsFriendOfEventOwnerToSeeAndOwnerToEditOrDelete
from .models import Comment
from .serializer import CommentSerializer, CommentDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsFriendOfEventOwnerToSeeAndOwnerToEditOrDelete]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [
        IsFriendOfEventOwnerToSeeAndOwnerToEditOrDelete]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']
