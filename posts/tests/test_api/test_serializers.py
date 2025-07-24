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
class TestSerializers:
    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user
        self.post = Post.objects.create(user=self.user, content='test content')

    def test_post_serializer(self):
        data = {
            'content':'test content.'
        }
        serializer = PostSerializer(data=data)

        assert serializer.is_valid() == True
    
    def test_post_media_serializer(self):
        fake_file = SimpleUploadedFile(
            name='test.jpeg',
            content=b'\x47\x49\x46',
            content_type='image/jpeg'
        )
        data = {
            'file':fake_file,
            'media_type':'image'
        }
        serializer = PostMediaSerializer(data=data)

        assert serializer.is_valid() == True
    
    def test_comment_serializer(self):
        data = {
            'post':self.post.id,
            'parent':None,
            'comment':'this is comment'
        }
        serializer = CommentSerializer(data=data)
        
        assert serializer.is_valid() == True

    def test_like_serializer(self):
        data = {
            'post':self.post.id,
            'status':True
        }
        serializer = LikeSerializer(data=data)

        assert serializer.is_valid() == True
    
    def test_share_serializer(self):
        data = {
            'post':self.post.id,
            'status':True
        }
        serializer = ShareSerializer(data=data)

        assert serializer.is_valid() == True
    
    def test_save_serializer(self):
        data = {
            'post':self.post.id,
            'status':True
        }
        serializer = SaveSerializer(data=data)

        assert serializer.is_valid() == True