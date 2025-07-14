from django.urls import path

from .views import (
    FollowToggleAPIView
)

urlpatterns = [
    path('follow/<str:username>/',FollowToggleAPIView.as_view(),name='follow'),
]