from django.urls import reverse
from django.contrib.auth import get_user_model
import pytest

User = get_user_model()

@pytest.fixture
def user(db):
    raw_password = 'Test12345%'
    user = User.objects.create_user(username='test1',email='test1@gmail.com',address='test1',
                                     city='test1',country='AF',password=raw_password)
    user.raw_password = raw_password
    
    return user

@pytest.fixture
def auth_client(user,client):
    client.force_login(user=user)
    return client

class SetUp:
    @pytest.fixture(autouse=True)
    def setUp(self, auth_client):
        self.client=auth_client

@pytest.mark.django_db
class TestSearchPostView(SetUp):
    def test_get_method(self):
        url = reverse('mvt_search:post_search')+'?q=hello'
        response = self.client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestSearchNetworkView(SetUp):
    def test_get_method(self):
        url =  reverse('mvt_search:network_search')+'?q=jan'
        response = self.client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestSearchNotificationView(SetUp):
    def test_get_method(self):
        url = reverse('mvt_search:notification_search')+'?q=liked'
        response = self.client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestSearchPostSaveView(SetUp):
    def test_get_method(self):
        url = reverse('mvt_search:post_save_search')+'?q=test'
        response = self.client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestSearchFiendView(SetUp):
    def test_get_method(self):
        url = reverse('mvt_search:friend_search')+'?q=test'
        response = self.client.get(url)

        assert response.status_code == 200