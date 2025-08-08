from django.urls import path,include

from search.mvt import urls as mvt_urls

urlpatterns = [
    path('search/', include((mvt_urls, 'mvt_search'), namespace='mvt_search'))
]