from django.urls import path

from .views import (
    ConnectionView
)

app_name = 'connections'

urlpatterns = [
    path('connection/',ConnectionView.as_view(),name='connection')
]