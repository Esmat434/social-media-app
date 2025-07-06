import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def user(db):
    password = 'Test12345%'
    user = User.objects.create_user(
            username='test',email='test@gmail.com',address='Timany',city='Kabul',country='AF',
            email_verified=True,password=password
            )
    user.raw_password = password
    return user

@pytest.fixture
def auth_client(user, client):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return client

class TestIsAuthenticatedPermissions:

    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
    
    def test_is_authenticated_permissions(self):
        url = reverse('api:profile', args=[self.user.id])
        response = self.client.get(url)

        assert response.status_code == 200

class TestIsNotAuthenticatedPermissions:

    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.client = client
        self.user = user
    
    def test_is_not_authenticated_permissions(self):
        data = {
            'username':self.user.username,
            'password':self.user.raw_password
        }
        url = reverse('mvt:login')
        response = self.client.get(url,data)

        assert response.status_code == 200