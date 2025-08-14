from django.urls import reverse

class TestUrls:
    def test_post_search_url(self):
        url = reverse('mvt_search:post_search')+'?q=test'

        assert url == '/search/post/?q=test'
    
    def test_network_search_url(self):
        url = reverse('mvt_search:network_search')+'?q=test'

        assert url == '/search/network/?q=test'
    
    def test_notification_search_url(self):
        url = reverse('mvt_search:notification_search')+'?q=test'

        assert url == '/search/notification/?q=test'
    
    def test_post_save_search_url(self):
        url = reverse('mvt_search:post_save_search')+'?q=test'

        assert url == '/search/saves/?q=test'
    
    def test_friend_search_url(self):
        url = reverse('mvt_search:friend_search')+'?q=test'

        assert url == '/search/friends/?q=test'