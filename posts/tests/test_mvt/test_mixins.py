import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

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

class TestPostView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client):
        self.client = auth_client
    
    def test_post_view(self):
        url = reverse('mvt_posts:create_post')
        response = self.client.get(url)
        
        assert response.status_code == 200