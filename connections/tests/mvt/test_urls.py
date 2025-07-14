from django.urls import reverse

def test_follow_url():
    url = reverse('mvt_connection:follow', args=['testuser'])
    assert url == '/follow/testuser/'

def test_unfollow_url():
    url = reverse('mvt_connection:un-follow', args=['testuser'])
    assert url == '/unfollow/testuser/'
