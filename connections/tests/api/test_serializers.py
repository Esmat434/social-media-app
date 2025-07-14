import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from connections.api.serializers import ConnectionSerializer

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

class TestConnectionSerializer:
    @pytest.fixture(autouse=True)
    def setUp(self,from_user,to_user):
        self.from_user = from_user
        self.to_user = to_user
        self.factory = APIRequestFactory()
    
    def test_connection_serializer(self):
        data = {
            'to_user':self.to_user.pk
        }
        request = self.factory.post('/fake-url/')
        request.user = self.from_user

        serializer = ConnectionSerializer(data=data, context={'request':request})

        assert serializer.is_valid() is True