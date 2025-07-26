from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.mvt.forms import (
    PostForm,PostMediaForm,CommentForm
)

class TestPostForm:
    def test_post_form_valid_data(self):
        data = {
            'content':'test content'
        }
        form = PostForm(data=data)

        assert form.is_valid() == True
    
    def test_post_form_invalid_data(self):
        data = {
            'content':'fuck you'
        }
        form = PostForm(data=data)

        assert form.is_valid() == False

class TestPostMediaForm:
    def test_post_media_form_validate(self):
        fake_file = SimpleUploadedFile(
            name='test.jpeg',
            content=b'\x47\x49\x46',
            content_type='image/jpeg'
        )

        files = {'file':fake_file}

        form = PostMediaForm(files=files)

        assert form.is_valid() == True
    
    def test_post_media_form_invalid_file_type(self):
        fake_file = SimpleUploadedFile(
            name='test.hdi',
            content=b'\x47\x49\x46',
            content_type='image/hdi'
        )

        files = {'file':fake_file}
         
        form = PostMediaForm(files=files)

        assert form.is_valid() == False
        
class TestCommentForm:
    def test_comment_form_validate_data(self):
        data = {
            'comment':'test comment'
        }
        form = CommentForm(data=data)

        assert form.is_valid() == True
    
    def test_comment_form_invalid_data(self):
        data = {
            'comment':'this is fuck comment'
        }
        form = CommentForm(data=data)

        assert form.is_valid() == False