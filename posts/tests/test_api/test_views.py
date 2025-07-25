import json
import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import (
    Post,Comment,Like,Share,Save
)

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
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = F'Bearer {access_token}'
    return client

@pytest.mark.django_db
class TestPostListCreateView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client):
        self.client = auth_client
    
    def test_get_method(self):
        url = reverse('api_posts:post_create')
        response = self.client.get(url)
        
        assert response.status_code == 200
    
    def test_post_method(self):
        data = {
            'content':'test content'
        }
        url = reverse('api_posts:post_create')
        response = self.client.post(url, data=data)

        assert response.status_code == 201

@pytest.mark.django_db
class TestPostRetrieveUpdateDeleteView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
        self.url = reverse('api_posts:post_delete_or_update', args=[self.post.pk])

    def test_get_method(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
    
    def test_put_method(self):
        data = {
            'content':'change data'
        }
        response = self.client.put(
            self.url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
    
    def test_delete_method(self): 
        response = self.client.delete(self.url)

        assert response.status_code == 204

@pytest.mark.django_db
class TestCommentCreateView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,user):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
        self.url = reverse('api_posts:comment_create')

    def test_post_method(self):
        data = {
            'post':self.post.pk,
            'comment':'test comment'
        }
        
        response = self.client.post(self.url, data=data)

        assert response.status_code == 201

@pytest.mark.django_db
class TestCommentRetrieveUpdateDeleteView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,user):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
        self.comment = Comment.objects.create(user=user, post=self.post, comment='test comment')
        self.url = reverse('api_posts:comment_delete_or_update', args=[self.comment.pk])
    
    def test_get_method(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_put_method(self):
        data = {
            'comment':'change comment'
        }
        response = self.client.put(
            self.url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 200
    
    def test_delete_method(self):
        response = self.client.delete(self.url)
        assert response.status_code == 204

@pytest.mark.django_db
class TestLikeCreateView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,user):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
        self.url = reverse('api_posts:like_create')

    def test_post_method(self):
        data = {
            'post':self.post.pk
        }
        response = self.client.post(self.url, data=data)

        assert response.status_code == 201
    

class TestLikeRetrieveDeleteView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,user):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
        self.like = Like.objects.create(user=user, post=self.post)
        self.url = reverse('api_posts:like_delete', args=[self.like.pk])

    def test_get_method(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
    
    def test_delete_method(self):
        resposne = self.client.delete(self.url)

        assert resposne.status_code == 204

@pytest.mark.django_db
class TestShareCreateView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,user):
        self.client = auth_client
        self.url = reverse('api_posts:share_create')
        self.post = Post.objects.create(user=user, content='test content')

    def test_post_method(self):
        data = {
            'post':self.post.pk
        }
        response = self.client.post(self.url, data=data)

        assert response.status_code == 201

class TestShareRetrieveDeleteView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,user):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
        self.share = Share.objects.create(user=user, post=self.post)
        self.url = reverse('api_posts:share_delete', args=[self.share.pk])

    def test_get_method(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
    
    def test_delete_method(self):
        response = self.client.delete(self.url)

        assert response.status_code == 204

@pytest.mark.django_db
class TestSaveCreateView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,user):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
        self.url = reverse('api_posts:save_create')
    
    def test_post_method(self):
        data = {
            'post':self.post.pk
        }
        response = self.client.post(self.url, data=data)

        assert response.status_code == 201
    
class TestSaveRetrieveDeleteView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,user):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
        self.save = Save.objects.create(user=user, post=self.post)
        self.url = reverse('api_posts:save_delete', args=[self.save.pk])
    
    def test_get_method(self):
        response = self.client.get(self.url)

        assert response.status_code == 200
    
    def test_delete_method(self):
        response = self.client.delete(self.url)

        assert response.status_code == 204