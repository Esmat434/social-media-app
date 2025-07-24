from django.db import models
from django.conf import settings
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"This post created by {self.user.username}"
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class PostMedia(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('image','Image'),
        ('video','Video')
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_media')
    file = models.FileField(upload_to='post_media/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default=MEDIA_TYPE_CHOICES[0][0])
    upload_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'PostMedia'
        verbose_name_plural = 'PostMedias'

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"post_{self.post.id} liked by {self.user.username}"
    
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = (
            'user','post'
        )

class Share(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_share')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_share')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} shared {self.post.id}"
    
    class Meta:
        verbose_name = 'Share'
        verbose_name_plural = 'Shares'
        unique_together = (
            'user','post'
        )

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='parent_comment')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} wrote comment to post_{self.post.id}"
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class Save(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_save')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_save')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"post_{self.post.id} saved by {self.user.username}"
    
    class Meta:
        verbose_name = 'Save'
        verbose_name_plural = 'Saves'
        unique_together = (
            'user','post'
        )