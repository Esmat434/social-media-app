from django.urls import reverse

class TestUrls:
    def test_search_post_url(self):
        url = reverse('api_search:post_search')+'?q=test'

        assert url == '/api/search/post/?q=test'
    
    def test_search_user_url(self):
        url = reverse('api_search:user_search')+'?q=test'

        assert url == '/api/search/user/?q=test'