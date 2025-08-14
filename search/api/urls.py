from django.urls import path

from .views import (
    SearchPostView,SearchUserView,SearchPostSaveView,SearchFriendView
)

app_name = 'api_search'

urlpatterns = [
    path('post/', SearchPostView.as_view(), name='post_search'),
    path('user/', SearchUserView.as_view(), name='user_search'),
    path('saves/', SearchPostSaveView.as_view(), name='post_save_search'),
    path('friends/', SearchFriendView.as_view(), name='friend_search')
]