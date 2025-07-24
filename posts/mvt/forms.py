from django import forms

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

        if extension not in self.VIDEO_TYPES and extension not in self.IMAGE_TYPES:
            raise forms.ValidationError("Your file type is incorrect.")
        
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