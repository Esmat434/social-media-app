from django.urls import path

from .views import (
    ConnectionAPIView
)

app_name = 'connections'

urlpatterns = [
    path('connection/',ConnectionAPIView.as_view(),name='connection'),
]