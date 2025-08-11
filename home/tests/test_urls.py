from django.urls import reverse

class TestUrls:
    def test_post_list_url(self):
        url = reverse('home:home-feed')

        assert url == '/'
    
    def test_network_list_url(self):
        url = reverse('home:networks')

        assert url == '/networks/'
    
    def test_notification_list_url(self):
        url = reverse('home:notifications')

        assert url == '/notifications/'
    
    def test_saves_url(self):
        url = reverse('home:saves')

        assert url == '/saves/'