from django.urls import path,include
from connections.api import urls as api_urls
from connections.mvt import urls as mvt_urls

urlpatterns = [
    path('api/',include((api_urls, 'api_connection'), namespace='api_connection')),
    path('',include((mvt_urls, 'mvt_connection'),namespace='mvt_connection')),
]