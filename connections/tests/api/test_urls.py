from django.urls import reverse

def test_follow_toggle_api_url():
    url = reverse('api_connection:follow', args=['testuser'])
    assert url == '/api/follow/testuser/'

def test_user_private_toggle__api_url():
    url =  reverse('api_connection:connection-request', args=['testuser'])
    assert url == '/api/connection/request/testuser/'