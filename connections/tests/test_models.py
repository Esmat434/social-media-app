import pytest

from django.contrib.auth import get_user_model
from django.db import IntegrityError,transaction

from connections.models import Connection

User = get_user_model()

@pytest.fixture
def from_user(db):
    return User.objects.create_user(username='test1',email='test1@gmail.com',address='test1',
                                     city='test1',country='AF')

@pytest.fixture
def to_user(db):
    return User.objects.create_user(username='test2',email='test2@gmail.com',address='test2',
                                     city='test2',country='AF')

class TestConnectionModel:
    def test_connection_creation(self, from_user, to_user):
        
        connection = Connection.objects.create(from_user=from_user, to_user=to_user)

        assert connection.from_user == from_user
        assert connection.to_user == to_user
        
        assert Connection.objects.count() == 1
        
        assert connection.created_at is not None

    def test_connection_str_method(self, from_user, to_user):
        
        connection = Connection.objects.create(from_user=from_user, to_user=to_user)
        
        expected_str = f"{from_user.username} follows {to_user.username}"
        assert str(connection) == expected_str

    def test_duplicate_connection_fails(self, from_user, to_user):
        
        Connection.objects.create(from_user=from_user, to_user=to_user)

        with pytest.raises(IntegrityError):

            with transaction.atomic():
                Connection.objects.create(from_user=from_user, to_user=to_user)
        
        assert Connection.objects.count() == 1