import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user(db):
    raw_password = 'Test1234%'
    user = User.objects.create_user(
            username='test',email='test@gmail.com',address='Timany',city='Kabul',country='AF',
            password=raw_password
        )
    user.raw_password=raw_password
    return user

@pytest.fixture
def auth_client(user,client):
    client.force_login(user)
    return client

class SetUp:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client):
        self.client = auth_client

@pytest.mark.django_db
class TestPostListView(SetUp):
    def test_get_method(self):
        url = reverse('home:home-feed')
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'home/home.html' in [t.name for t in response.templates]
    
@pytest.mark.django_db
class TestNetworkListView(SetUp):
    def test_get_method(self):
        url = reverse('home:networks')
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'home/network.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestNotificationListView(SetUp):
    def test_get_method(self):
        url = reverse('home:notifications')
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'home/notification.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestSaveListView(SetUp):
    def test_get_method(self):
        url = reverse('home:saves')
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'home/post_save.html' in [t.name for t in response.templates]