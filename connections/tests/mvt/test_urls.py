from django.urls import reverse

def test_follow_url():
    url = reverse('mvt_connection:follow', args=['testuser'])
    assert url == '/follow/testuser/'

def test_follow_private_request():
    url = reverse('mvt_connection:follow-private-request', args=['testuser'])
    assert url == '/follow/testuser/private_request/'

def test_follow_private_accept():
    url = reverse('mvt_connection:follow-private-accept', args=['testuser'])
    assert url == '/follow/testuser/private_accept/'

def test_unfollow_url():
    url = reverse('mvt_connection:un-follow', args=['testuser'])
    assert url == '/unfollow/testuser/'
