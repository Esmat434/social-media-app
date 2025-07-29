from django.urls import path

from .views import (
    FollowView,UserPrivateRequestView,UserPrivateAcceptRequestView,UserPrivateRejectRequestView,
    UnFollowView
)

urlpatterns = [
    path('follow/<str:username>/',FollowView.as_view(),name='follow'),
    path('follow/<str:username>/private_request/',UserPrivateRequestView.as_view(),name='follow-private-request'),
    path('follow/<str:username>/private_accept/',UserPrivateAcceptRequestView.as_view(),name='follow-private-accept'),
    path('follow/<str:username>/private_reject/',UserPrivateRejectRequestView.as_view(),name='follow-private-reject'),
    path('unfollow/<str:username>/',UnFollowView.as_view(),name='un-follow'),
]