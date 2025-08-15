import uuid
from django.urls import reverse

class TestUrls:
    def test_register_url(self):
        url = reverse('api:register')

        assert url == '/api/register/'
    
    def test_login_url(self):
        url = reverse('api:login')

        assert url == '/api/login/'
    
    def test_logout_url(self):
        url = reverse('api:logout')

        assert url == '/api/logout/'
    
    def test_profile_url(self):
        url = reverse('api:profile', args=[1])

        assert url == f'/api/profile/{1}/'
    
    def test_profile_update_url(self):
        url = reverse('api:profile-update', args=[1])

        assert url == f'/api/profile/{1}/update/'
    
    def test_change_password_url(self):
        url = reverse('api:change_password')

        assert url == f'/api/change_password/'
    
    def test_forgot_password_url(self):
        url = reverse('api:forgot_password')

        assert url == '/api/forgot_password/'
    
    def test_friends_url(self):
        url = reverse('api:friends')

        assert url == '/api/friends/'