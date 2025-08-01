from django.urls import path

from .views import (
    PostListView,NetworkListView,NotificationListView,SaveListView
)

app_name = 'home'

urlpatterns = [
    path('', PostListView.as_view(), name='home-feed'),
    path('networks/', NetworkListView.as_view(), name='networks'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('saves/', SaveListView.as_view(), name='saves/')
]