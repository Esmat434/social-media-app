import pytest
from django.urls import reverse

from accounts.models import (
    CustomUser
)

@pytest.fixture
def user(db):
    password='Test12345%'
    user = CustomUser.objects.create_user(
            username='test',email='test@gmail.com',address='Timany',city='Kabul',country='AF',            
            password=password
            )
    user.raw_password = password
    return user

@pytest.mark.django_db
class TestLoginRequiredMixin:
    def test_render_template_login_profile_view(self,user,client):
        login_successful = client.login(username=user.username, password=user.raw_password)

        assert login_successful == True

        url = reverse('mvt:profile')
        response = client.get(url)

        assert response.status_code == 200

    def test_redirect_no_login_profile_view(self,client):
        url = reverse('mvt:profile')
        response = client.get(url)

        assert response.status_code == 302
        assert response.url == reverse('mvt:login')

@pytest.mark.django_db
class TestLogoutRequiredMixin:
    def test_render_template_register_view(self,client):
        url = reverse('mvt:login')
        response = client.get(url)

        assert response.status_code == 200
    
    def test_redirect_home_register_view(self,user,client):
        login_successfull = client.login(username=user.username, password=user.raw_password)

        assert login_successfull == True

        url = reverse('mvt:login')
        response = client.get(url)

        assert response.status_code == 302

@pytest.mark.django_db
class TestAccountVerifiedBeforeLoginMixin:
    def test_render_login_page_login_view(self,user,client):
        user.email_verified = True
        user.save()

        url = reverse('mvt:login')
        response = client.get(url)

        assert response.status_code == 200
        assert 'accounts/login.html' in [t.name for t in response.templates]
    
    def test_render_account_verified_message_page_login_view(self,user,client):
        user.email_verified = False
        user.save()

        url = reverse('mvt:login')
        data = {
            'username':user.username,
            'password':user.raw_password
        }
        response = client.post(url,data)

        assert response.status_code == 200
        assert 'accounts/account_verified_message.html' in [t.name for t in response.templates]