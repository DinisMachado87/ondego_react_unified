from django.urls import path
from joinings import views


urlpatterns = [
    path('joinings/', views.JoiningList.as_view()),
    path('joinings/<int:pk>/', views.JoiningDetail.as_view()),
]
