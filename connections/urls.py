from django.urls import path,include

urlpatterns = [
    path('api/',include('api.urls',namespace='api')),
    path('',include('mvt.urls',namespace='mvt')),
]