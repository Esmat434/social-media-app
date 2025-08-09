from django.urls import path,include

from search.mvt import urls as mvt_urls
from search.api import urls as api_urls

urlpatterns = [
    path('search/', include((mvt_urls, 'mvt_search'), namespace='mvt_search')),
    path('api/search/', include((api_urls, 'api_search'), namespace='api_search')),
]