from django.urls import path

from .views import (
    FollowView,UnFollowView
)

app_name = 'connections'

urlpatterns = [
    path('follow/<str:username>/',FollowView.as_view(),name='follow'),
    path('unfollow/<str:username>/',UnFollowView.as_view(),name='un-follow'),
]