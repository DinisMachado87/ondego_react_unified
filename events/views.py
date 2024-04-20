from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer
from ondego_api.permissions import IsOwnerOrReadOnly


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.annotate(
        let_me_see_count=Count('joining', filter=Q(
            joining__joining_status='3'), distinct=True),
        not_joining_count=Count('joining', filter=Q(
            joining__joining_status='1'), distinct=True),
        joining_count=Count('joining', filter=Q(
            joining__joining_status='2'), distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner',
        'what_title',
        'when_start',
        'when_end',
    ]
    ordering_fields = [
        'when_start',
        'when_end',
        'joining_count',
        'comments_count'
    ]
    search_fields = [
        'owner__username',
        'what_title',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Event.objects.annotate(
        let_me_see_count=Count('joining', filter=Q(
            joining__joining_status='3'), distinct=True),
        not_joining_count=Count('joining', filter=Q(
            joining__joining_status='1'), distinct=True),
        joining_count=Count('joining', filter=Q(
            joining__joining_status='2'), distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
