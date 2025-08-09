from django.urls import path

from .views import (
    SearchPostView,SearchUserView
)

app_name = 'api_search'

urlpatterns = [
    path('post/', SearchPostView.as_view(), name='post_search'),
    path('user/', SearchUserView.as_view(), name='user_search')
]