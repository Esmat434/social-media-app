from django.urls import path

from .views import (
    SearchPostView
)

urlpatterns = [
    path('post/', SearchPostView.as_view(), name='post_search'),
]