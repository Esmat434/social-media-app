import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from posts.models import (
    Post
)

from posts.api.serializers import (
    PostSerializer,PostMediaSerializer,CommentSerializer,LikeSerializer,ShareSerializer,
    SaveSerializer
)

User = get_user_model()

@pytest.fixture
def user(db):
    raw_password = 'Test12345%'
    user = User.objects.create_user(username='test1',email='test1@gmail.com',address='test1',
                                     city='test1',country='AF',password=raw_password)
    user.raw_password = raw_password
    return user

@pytest.mark.django_db
class TestPostSerializer:
    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')

    def test_post_serializer_validate_data(self):
        valid_data = {
            'content':'test content.'
        }

        serializer = PostSerializer(data=valid_data)

        assert serializer.is_valid(raise_exception=True)

        post_instance = serializer.save(user=self.user)

        assert post_instance.user == self.user
        assert post_instance.content == 'test content.'
    
    def test_post_serializer_invalid_data(self):
        data = {
            'content':'this is some fuck word'
        }

        serializer = PostSerializer(data=data)

        assert not serializer.is_valid()
        
        assert 'content' in serializer.errors

class TestMediaSerializer:
    def test_post_media_serializer_validate_data(self):
        small_content = b'a' * (4 * 1024 * 1024)
        fake_file = SimpleUploadedFile(
            name='test.jpeg',
            content=small_content,
            content_type='image/jpeg'
        )
        data = {
            'file':fake_file
        }
        serializer = PostMediaSerializer(data=data)

        assert serializer.is_valid() == True
    
    def test_post_media_serializer_invalid_data(self):
        large_content = b'a' * (50 * 1024 * 1024)
        fake_file = SimpleUploadedFile(
            name='test.jpeg',
            content=large_content,
            content_type='image/jpeg'
        )
        data = {
            'file':fake_file
        }
        serializer = PostMediaSerializer(data=data)

        assert serializer.is_valid() == False

@pytest.mark.django_db
class TestCommentSerializer:
    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')

    def test_comment_serializer_validate_data(self):
        valid_data = {
            'post':self.post.id,
            'parent':None,
            'comment':'this is comment'
        }

        valid_serializer = CommentSerializer(data=valid_data)

        assert valid_serializer.is_valid(), valid_serializer.errors

        comment_instance = valid_serializer.save(user=self.user)

        assert comment_instance.user == self.user
        assert comment_instance.comment == 'this is comment'

    def test_comment_serializer_invalid_data(self):
        data = {
            'post':self.post.pk,
            'parent':None,
            'comment':'this is fuck comment'
        }

        serializer = CommentSerializer(data=data)

        assert not serializer.is_valid()

        assert 'comment' in serializer.errors

@pytest.mark.django_db
class TestLikeSerializer:
    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')

    def test_like_serializer(self):
        data = {
            'post':self.post.id,
            'status':True
        }
        serializer = LikeSerializer(data=data)

        assert serializer.is_valid() == True
    
@pytest.mark.django_db
class TestShareSerializer:
    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')

    def test_share_serializer(self):
        data = {
            'post':self.post.id,
            'status':True
        }
        serializer = ShareSerializer(data=data)

        assert serializer.is_valid() == True
    
@pytest.mark.django_db
class TestSaveSerializer:
    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')

    def test_save_serializer(self):
        data = {
            'post':self.post.id,
            'status':True
        }
        serializer = SaveSerializer(data=data)

        assert serializer.is_valid() == True