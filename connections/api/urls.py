from django.urls import path

from .views import (
    FollowToggleAPIView,UserPrivateToggleAPIView
)

urlpatterns = [
    path('follow/<str:username>/',FollowToggleAPIView.as_view(),name='follow'),
    path('connection/request/<str:username>/',UserPrivateToggleAPIView.as_view(),name='connection-request'),
]