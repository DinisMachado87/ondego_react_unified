from django.urls import path
from friends import views


urlpatterns = [
    path('friends/', views.FriendsList.as_view()),
    path('friends/<int:pk>/', views.FriendDetail.as_view()),
    path('friends_requests/', views.FriendsRequest.as_view()),
    path('friends_requests/<int:pk>/', views.FriendRequestDetail.as_view()),
]
