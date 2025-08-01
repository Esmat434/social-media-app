import pytest
from django.urls import reverse
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

@pytest.fixture
def auth_client(actor_user,client):
    client.force_login(actor_user)
    return client

class TestDeleteNotoficationView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,actor_user,recipient_user):
        self.client = auth_client
        self.user = actor_user
        self.post = Post.objects.create(user=actor_user, content='test content')
        self.notification = Notification.objects.create(
                recipient=recipient_user, 
                actor=actor_user, 
                content_type=ContentType.objects.get_for_model(self.post), 
                object_id=self.post.id
            )

    def test_post_method(self):
        url = reverse('notification:process-notification', args=[self.notification.pk])
        response = self.client.post(url)

        assert response.status_code == 302