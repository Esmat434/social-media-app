import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from connections.models import Connection

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
    client.force_login(from_user)
    return client

@pytest.mark.django_db
class TestFollowView:
    @pytest.fixture(autouse=True)
    def setUp(self,to_user,auth_client):
        self.to_user = to_user
        self.client = auth_client
    
    def test_follow_view(self):
        url = reverse('mvt_connection:follow', args=[self.to_user.username])
        response = self.client.post(url)

        assert response.status_code == 201

@pytest.mark.django_db
class TestUserPrivateRequestView:
    @pytest.fixture(autouse=True)
    def setUp(self,to_user,auth_client):
        self.to_user=to_user
        self.client=auth_client
    
    def test_post_method(self):
        url = reverse('mvt_connection:follow-private-request', args=[self.to_user.username])
        response = self.client.post(url)

        assert response.status_code == 201

@pytest.mark.django_db
class TestUserPrivateAcceptedRequestView:
    @pytest.fixture(autouse=True)
    def setUp(self,from_user,to_user,auth_client):
        self.to_user=to_user
        self.client=auth_client
        self.connection = Connection.objects.create(from_user=to_user, to_user=from_user, status=Connection.ConnectionStatus.PENDING)

    def test_post_method(self):
        url = reverse('mvt_connection:follow-private-accept', args=[self.to_user.username])
        response = self.client.post(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestUserPrivateRejectedRequestView:
    @pytest.fixture(autouse=True)
    def setUp(self,from_user,to_user,auth_client):
        self.to_user = to_user
        self.client = auth_client
        self.connection = Connection.objects.create(from_user=to_user, to_user=from_user)
    
    def test_post_method(self):
        url = reverse('mvt_connection:follow-private-reject', args=[self.to_user.username])
        response = self.client.post(url)

        assert response.status_code == 204

@pytest.mark.django_db
class TestUnFollowView:
    @pytest.fixture(autouse=True)
    def setUp(self,from_user,to_user,auth_client):
        self.from_user = from_user
        self.to_user = to_user
        self.client = auth_client
        self.connection = Connection.objects.create(from_user=self.from_user, to_user=self.to_user, status=Connection.ConnectionStatus.ACCEPTED)
    
    def test_unfollow_view(self):
        url = reverse('mvt_connection:un-follow', args=[self.to_user.username])
        response = self.client.post(url)

        assert response.status_code == 204