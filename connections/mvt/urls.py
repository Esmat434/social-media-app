from django.urls import path

from .views import (
    ConnectionView
)

app_name = 'connection'

urlpatterns = [
    path('connection/',ConnectionView.as_view(),name='connection')
]