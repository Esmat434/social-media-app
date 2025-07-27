from django import forms

from posts.algorithms.validators import (
    word_filtering
)

from posts.models import (
    Post,PostMedia,Comment
)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'content',
        )
        widgets = {
            'content':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter your content.'})
        }
    
    def clean_content(self):
        content = self.cleaned_data['content']
        
        text_status = word_filtering(content)
        
        if text_status:
            raise forms.ValidationError("Your content is not legal and politness.")
        
        return content
    
class PostMediaForm(forms.ModelForm):
    VIDEO_TYPES = ['mp4','mkv','avi','webm']
    IMAGE_TYPES = ['jpg','jpeg','png','gif','svg']
    class Meta:
        model = PostMedia
        fields = (
            'file',
        )
        widgets = {
            'file': forms.FileInput(attrs={'class':'form-control','placeholder':'Enter your file.'})
        }
    
    def clean_file(self):
        file = self.cleaned_data['file']

        extension = file.name.split('.')[-1].lower()
        is_image = extension in self.IMAGE_TYPES
        is_video = extension in self.VIDEO_TYPES

        if not is_image and not is_video:
            raise forms.ValidationError("this file type does not support please select image or video.")
        
        IMAGE_MAX_SIZE = 5 * 1024 * 1024
        VIDEO_MAX_SIZE = 50 * 1024 * 1024

        if is_image and file.size > IMAGE_MAX_SIZE:
            raise forms.ValidationError(f"your image size {file.size / 1024 / 1024:.2f} MB")
        
        if is_video and file.size > VIDEO_MAX_SIZE:
            raise forms.ValidationError(f"your video size {file.size / 1024 / 1024:.2f} MB")
        
        return file
    
    def save(self, commit=True):
        post_media = super().save(commit=False)
        
        extension = post_media.file.name.split('.')[-1].lower()

        if extension in self.VIDEO_TYPES:
            post_media.media_type = 'video'
        else:
            post_media.media_type = 'image'
        
        if commit:
            post_media.save()
        
        return post_media

    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'comment',
        )
        widgets = {
            'comment':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter your comment.'})
        }
    
    def clean_comment(self):
        comment = self.cleaned_data['comment']

        text_status = word_filtering(comment)
        if text_status:
            raise forms.ValidationError("Your comment is not legal and politness.")
        
        return comment