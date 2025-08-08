from django.urls import reverse

class TestUrls:
    def test_post_search_url(self):
        url = reverse('mvt_search:post_search')+'?q=hi'

        assert url == '/search/post/?q=hi'
    
    def test_network_search_url(self):
        url = reverse('mvt_search:network_search')+'?q=hi'

        assert url == '/search/network/?q=hi'
    
    def test_notification_search_url(self):
        url = reverse('mvt_search:notification_search')+'?q=hi'

        assert url == '/search/notification/?q=hi'