import pytest
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from posts.models import (
    Post
)
from notification.models import (
    Notification
)

User = get_user_model()

@pytest.fixture
def actor_user(db):
    raw_password = 'Test12345%'
    user = User.objects.create_user(username='test1',email='test1@gmail.com',address='test1',
                                     city='test1',country='AF',password=raw_password)
    return user

@pytest.fixture
def recipient_user(db):
    raw_password = 'Test12345%'
    user = User.objects.create_user(username='test2',email='test2@gmail.com',address='test1',
                                     city='test1',country='AF',password=raw_password)
    return user

@pytest.mark.django_db
class TestNotificationModel:
    @pytest.fixture(autouse=True)
    def setUp(self,actor_user,recipient_user):
        self.actor = actor_user
        self.recipient = recipient_user
        self.post = Post.objects.create(user=actor_user, content='test content')

    def test_notification_model(self):
        notification = Notification.objects.create(
                recipient=self.recipient, 
                actor=self.actor, 
                target=self.post
            )
        
        assert notification.recipient == self.recipient
        assert notification.actor == self.actor
        assert notification.target == self.post