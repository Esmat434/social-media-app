from django.urls import path,include
from .api import urls as api_urls
from .mvt import urls as mvt_urls

urlpatterns = [
    path('api/',include((api_urls,'api'),namespace='api')),
    path('',include((mvt_urls,'mvt'),namespace='mvt'))
]
