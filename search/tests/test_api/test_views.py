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
def auth_client(user,client):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return client

class SetUp:
    @pytest.fixture(autouse=True)
    def setUp(self, auth_client):
        self.client = auth_client

@pytest.mark.django_db
class TestSearchPostView(SetUp):
    def test_get_method(self):
        url = reverse('api_search:post_search')+'?q=test'
        response = self.client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestSearchUserView(SetUp):
    def test_get_method(self):
        url = reverse('api_search:user_search')+'?q=test'
        response = self.client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestSearchPostSaveView(SetUp):
    def test_get_method(self):
        url = reverse('api_search:post_save_search')+'?q=test'
        response = self.client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class testSearchFriendView(SetUp):
    def test_get_method(self):
        url = reverse('api_search:friend_search')+'?q=test'
        response = self.client.get(url)

        assert response.status_code == 200