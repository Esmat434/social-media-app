from django.urls import path

from .views import (
    SearchPostView,SearchNetworkView,SearchNotificationView,SearchPostSaveView,SearchFriendView
)

app_name = 'mvt_search'

urlpatterns = [
    path('post/', SearchPostView.as_view(), name='post_search'),
    path('network/', SearchNetworkView.as_view(), name='network_search'),
    path('notification/', SearchNotificationView.as_view(), name='notification_search'),
    path('saves/', SearchPostSaveView.as_view(), name='post_save_search'),
    path('friends/', SearchFriendView.as_view(), name='friend_search'),
]