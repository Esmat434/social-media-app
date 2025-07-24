from django.urls import path,include

from .mvt import urls as mvt_urls
from .api import urls as api_urls

urlpatterns = [
    path('api/', include((api_urls, 'api_posts'), namespace='api_posts')),
    path('', include((mvt_urls, 'mvt_posts'), namespace='mvt_posts')),
]