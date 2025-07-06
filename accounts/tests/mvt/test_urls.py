import uuid
from django.urls import reverse

def test_register_url():
    url = reverse('mvt:register')
    assert url == '/register/'
    
def test_login_url():
    url = reverse('mvt:login')
    assert url == '/login/'

def test_logout_url():
    url = reverse('mvt:logout')
    assert url == '/logout/'

def test_profile_url():
    url = reverse('mvt:profile')
    assert url == '/profile/'

def test_profile_update_url():
    url = reverse('mvt:profile_update')
    assert url == '/profile/update/'

def test_account_verified_url():
    token = uuid.uuid4()
    url = reverse('mvt:account_verified',args=[token])
    assert url == f'/account_verified/{token}/'

def test_create_change_password_token_url():
    url = reverse('mvt:create_change_password_token')
    assert url == '/create_change_password_token/'

def test_change_password_url():
    token = uuid.uuid4()
    url = reverse('mvt:change_password', args=[token])
    assert url == f'/change_password/{token}/'

def test_cerate_forgot_password_token_url():
    url = reverse('mvt:create_forgot_password_token')
    assert url == '/create_forgot_password_token/'

def test_forgot_password():
    token = uuid.uuid4()
    url = reverse('mvt:forgot_password', args=[token])
    assert url == f'/forgot_password/{token}/'