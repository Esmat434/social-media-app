from django.urls import reverse

class TestUrls:
    def test_search_post_url(self):
        url = reverse('api_search:post_search')+'?q=test'

        assert url == '/api/search/post/?q=test'
    
    def test_search_user_url(self):
        url = reverse('api_search:user_search')+'?q=test'

        assert url == '/api/search/user/?q=test'
    
    def test_post_save_search_url(Self):
        url = reverse('api_search:post_save_search')+'?q=test'

        assert url == '/api/search/saves/?q=test'
    
    def test_friend_search_url(self):
        url = reverse('api_search:friend_search')+'?q=test'

        assert url == '/api/search/friends/?q=test'