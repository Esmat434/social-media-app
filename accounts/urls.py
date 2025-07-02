from django.urls import path,include

urlpatterns = [
    path('api/',include('accounts.api.urls',namespace='api')),
    path('',include('accounts.mvt.urls',namespace='mvt'))
]
