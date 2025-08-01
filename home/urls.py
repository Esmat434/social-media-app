from django.urls import path

from .views import (
    PostListView,NetworkListView
)

app_name = 'home'

urlpatterns = [
    path('', PostListView.as_view(), name='home-feed'),
]