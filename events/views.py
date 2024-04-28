from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer
from ondego_api.permissions import IsFriendToSeeAndOwnerToEditOrDelete
from django.utils import timezone
from datetime import timedelta
from django_filters import FilterSet, BooleanFilter, NumberFilter


class EventFilter(FilterSet):
    '''
    Filters events that are going on or will start in the next two hours
    '''
    going_on = BooleanFilter(method='filter_going_on')
    joining_status = NumberFilter(field_name='joining__joining_status')
    joining_owner = NumberFilter(field_name='joining__owner__id')

    class Meta:
        model = Event
        fields = [
            'owner',
            'when_start',
            'when_end',
            'going_on',
        ]

    def filter_going_on(self, queryset, name, value):
        '''
        Filter events that are going on or will start in the next two hours
        '''
        if value:
            now = timezone.now()
            two_hours_later = now + timedelta(hours=2)
            return queryset.filter(when_start__lte=two_hours_later, when_end__gte=now)
        return queryset

class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsFriendToSeeAndOwnerToEditOrDelete]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Include events where the request.user is a friend of the event owner or the owner itself
            return Event.objects.filter(Q(owner__user_friends__friend=user) | Q(owner=user)).annotate(
                let_me_see_count=Count('joining', filter=Q(
                    joining__joining_status='3'), distinct=True),
                not_joining_count=Count('joining', filter=Q(
                    joining__joining_status='1'), distinct=True),
                joining_count=Count('joining', filter=Q(
                    joining__joining_status='2'), distinct=True),
                comments_count=Count('comment', distinct=True)
            ).order_by('-created_at')
        # If the user is not authenticated, return an empty queryset
        return Event.objects.none()
    
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner',
        'when_start',
        'when_end',
        'joining_status',
        'joining_owner',
    ]
    ordering_fields = [
        'when_start',
        'when_end',
        'joining_count',
        'comments_count'
        'owner__last_login'
    ]
    search_fields = [
        'owner__username',
        'what_title',
    ]
    filterset_class = EventFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsFriendToSeeAndOwnerToEditOrDelete]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Include events where the request.user is a friend of the event owner or the owner itself
            return Event.objects.filter(Q(owner__user_friends__friend=user) | Q(owner=user)).annotate(
                let_me_see_count=Count('joining', filter=Q(
                    joining__joining_status='3'), distinct=True),
                not_joining_count=Count('joining', filter=Q(
                    joining__joining_status='1'), distinct=True),
                joining_count=Count('joining', filter=Q(
                    joining__joining_status='2'), distinct=True),
                comments_count=Count('comment', distinct=True)
            ).order_by('-created_at')
        # If the user is not authenticated, return an empty queryset
        return Event.objects.none()
    
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = EventFilter
    filterset_fields = [
        'owner',
        'when_start',
        'when_end',
    ]
    ordering_fields = [
        'when_start',
        'when_end',
        'joining_count',
        'comments_count'
        'owner__last_login'
    ]
    search_fields = [
        'owner__username',
        'what_title',
    ]
