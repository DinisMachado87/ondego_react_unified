from rest_framework import generics, permissions
from ondego_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from friends.models import Friend
from .serializer import CommentSerializer, CommentDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q



class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']


    def get_queryset(self):
        user = self.request.user
        friend_ids = user.friend_friends.all().values_list('owner_id', flat=True)
        return Comment.objects.filter(event__owner_id__in=friend_ids)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']


def get_queryset(self):
    user = self.request.user
    friend_ids = user.friend_friends.all().values_list('owner_id', flat=True)
    return Comment.objects.filter(event__owner_id__in=friend_ids)
