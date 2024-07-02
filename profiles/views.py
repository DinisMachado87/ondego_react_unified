from django.db.models import Count
from rest_framework import status, permissions, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from ondego_api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F


class ProfileList(generics.ListAPIView):
    '''
    List all profiles
    '''
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        joined_events_count=Count('owner__joining', distinct=True),
        friends_count=Count('owner__user_friends', distinct=True),
        last_login=F('owner__last_login')
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ['owner__username']
    ordering_fields = [
        'owner__username',
        'events_count',
        'joined_events_count',
        'last_login',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    '''
    Retrieve, update or delete a profile instance
    '''
    queryset = Profile.objects.annotate(
        events_count=Count('owner__event', distinct=True),
        joined_events_count=Count('owner__joining', distinct=True),
        friends_count=Count('owner__user_friends', distinct=True),
        last_login=F('owner__last_login')
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
