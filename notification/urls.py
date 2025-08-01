from django.urls import path

from .views import DeleteNotificatoinView

app_name = 'notification'

urlpatterns = [
    path('<int:pk>/process/', DeleteNotificatoinView.as_view(), name='process-notification')
]