from django.db import models
from django.conf import settings
# Create your models here.

class Connection(models.Model):
    
    class ConnectionStatus(models.TextChoices):
        PENDING = 'pending',
        ACCEPTED = 'accepted', 
        REJECTED = 'rejected', 
    
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following_connections'
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower_connections'
    )
    status = models.CharField(max_length=20, choices=ConnectionStatus.choices, default=ConnectionStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user','to_user')
    
    def __str__(self):
        return f"{self.from_user.username} follows {self.to_user.username}"