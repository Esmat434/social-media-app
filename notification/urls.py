from django.urls import path

from .views import DeleteNotificatoinView

app_name = 'home'

urlpatterns = [
    path('<int:pk>/process/', DeleteNotificatoinView.as_view(), name='process-notification')
]