import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def from_user(db):
    raw_password = 'Test12345%'
    user = User.objects.create_user(username='test1',email='test1@gmail.com',address='test1',
                                    city='test1',country='AF',password=raw_password)
    user.raw_password=raw_password
    return user

@pytest.fixture
def to_user(db):
    return User.objects.create_user(username='test2',email='test2@gmail.com',address='test2',
                                    city='test2',country='AF')

@pytest.fixture
def auth_client(from_user,client):
    refresh = RefreshToken.for_user(from_user)
    access_token = str(refresh.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return client

@pytest.mark.django_db
class TestCustomIsAuthenticate:
    @pytest.fixture(autouse=True)
    def setUp(self,from_user,to_user,auth_client):
        self.from_user = from_user
        self.to_user = to_user
        self.client = auth_client

    def test_success_custom_is_authenticate(self):
        url = reverse('api_connection:follow', args=[self.to_user.username])
        response = self.client.post(url)

        assert response.status_code == 201