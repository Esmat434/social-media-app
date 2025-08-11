import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import (
    Post,Comment
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
    client.force_login(user=user)
    return client

class TestPostView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client):
        self.client = auth_client
    
    def test_get_method_post_view(self):
        url = reverse('mvt_posts:create_post')
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'posts/post_create.html' in [t.name for t in response.templates]
    
    def test_post_method_post_view(self):
        data = {
            'content':'test content.'
        }
        url = reverse('mvt_posts:create_post')
        response = self.client.post(url, data=data)

        assert response.status_code == 302
    
class TestEditPostView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
        self.post = Post.objects.create(user=self.user,content='test content')
    
    def test_get_method_edit_post_view(self):
        url = reverse('mvt_posts:edit_post', args=[self.post.pk])
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'posts/post_edit.html' in [t.name for t in response.templates]
    
    def test_post_method_edit_post_view(self):
        data = {
            'content':'change post'
        }
        url = reverse('mvt_posts:edit_post', args=[self.post.pk])
        response = self.client.post(url, data=data)

        assert response.status_code == 302

class TestDeletePostView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')
    
    def test_post_method_delete_post_view(self):
        url = reverse('mvt_posts:delete_post', args=[self.post.pk])
        response = self.client.post(url)

        assert response.status_code == 302

class TestCreateCommentView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,user):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
    
    def test_create_comment_view(self):
        data = {
            'comment':'test comment'
        }
        url = reverse('mvt_posts:create_comment', args=[self.post.id])
        response = self.client.post(url, data=data)

        assert response.status_code == 201

class TestCreateParentCommentView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.post = Post.objects.create(user=user, content='test content')
        self.comment = Comment.objects.create(user=user, post=self.post, comment='test comment')
    
    def test_post_method_create_parent_comment_view(self):
        data = {
            'comment':'this is good'
        }
        url = reverse('mvt_posts:create_parent_comment', args=[self.post.pk,self.comment.pk])
        response = self.client.post(url, data=data)

        assert response.status_code == 201

class TestEditCommentView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')
        self.comment = Comment.objects.create(user=self.user, post=self.post, comment='test comment')
    
    def test_post_method_edit_comment_view(self):
        data = {
            'comment':'test change comment'
        }
        url = reverse('mvt_posts:edit_comment', args=[self.comment.pk])
        response = self.client.post(url, data=data)

        assert response.status_code == 200
    
class TestDeleteCommentView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')
        self.comment = Comment.objects.create(user=self.user, post=self.post, comment='test comment')
    
    def test_post_method(self):
        url = reverse('mvt_posts:delete_comment', args=[self.comment.pk])
        response = self.client.post(url)

        assert response.status_code == 200

class TestCreateLikeView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')
    
    def test_post_method_like_view(self):
        url = reverse('mvt_posts:create_like', args=[self.post.pk])
        response = self.client.post(url)

        assert response.status_code == 201
    
class TestCreateShareView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content.')
    
    def test_post_method_create_like_view(self):
        url = reverse('mvt_posts:create_share', args=[self.post.pk])
        response = self.client.post(url)

        assert response.status_code == 201

class TestCreateSaveView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')
    
    def test_post_method_create_save_view(self):
        url = reverse('mvt_posts:create_save', args=[self.post.pk])
        response = self.client.post(url)

        assert response.status_code == 201