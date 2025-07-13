from django.urls import path

from .views import (
    FollowToggleAPIView
)

app_name = 'connections'

urlpatterns = [
    path('follow/<str:username>/',FollowToggleAPIView.as_view(),name='follow'),
]