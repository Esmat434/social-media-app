import pytest

from django.contrib.auth import get_user_model

from posts.models import (
    Post,PostMedia,Comment,Like,Share,Save
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
class TestModels:
    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user
        self.post = Post.objects.create(user=self.user,content='Test content.')
    def test_post_model(self):
        post = Post.objects.create(user=self.user,content='Test content.')

        assert post.user == self.user
        assert post.user.username == 'test1'
        assert post.content == 'Test content.'
    
    def test_post_media_model(self):
        file = 'c://dell/media.jpeg'
        post_media = PostMedia.objects.create(post=self.post, file=file,media_type='image')

        assert post_media.post == self.post
        assert post_media.file == file
        assert post_media.media_type == 'image'

    def test_comment_model(self):
        parent_comment = Comment.objects.create(user=self.user, post=self.post, comment='test parent comment.')
        comment = Comment.objects.create(user=self.user, post=self.post, parent=parent_comment, comment='test')
        
        assert parent_comment.user == self.user
        assert parent_comment.post == self.post
        assert parent_comment.parent == None
        assert parent_comment.comment == 'test parent comment.'

        assert comment.user == self.user
        assert comment.post == self.post
        assert comment.parent == parent_comment
        assert comment.comment == 'test'
    
    def test_like_model(self):
        like = Like.objects.create(user=self.user, post=self.post)

        assert like.user == self.user
        assert like.post == self.post
        assert like.status == True
    
    def test_share_model(self):
        share = Share.objects.create(user=self.user, post=self.post)

        assert share.user == self.user
        assert share.post == self.post
        assert share.status == True
    
    def test_save_model(self):
        save = Save.objects.create(user=self.user, post=self.post)

        assert save.user == self.user
        assert save.post == self.post
        assert save.status == True