from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import (
    Post,Comment,Like,Share
)

from notification.models import (
    Notification
)


@receiver(post_save, sender=Post)
def send_notification_after_save_post(sender, instance, created, **kwargs):
    if created:
        actor = instance.user
        # follower_connections شامل ارتباطاتی است که actor در آنها to_user است
        # ما باید from_user را به عنوان گیرنده بگیریم
        followers = actor.follower_connections.filter(status='accepted')

        for connection in followers:
 
            recipient = connection.from_user
            
            if recipient != actor:
                Notification.objects.create(
                    actor=actor,
                    recipient=recipient,
                    verb='published new post',
                    target=instance
                )

@receiver(post_save, sender=Comment)
def send_notification_after_save_comment(sender, instance, created, **kwargs):
    if created:
        actor = instance.user
        
        if instance.parent:
            recipient = instance.parent.user
            verb = 'gived response to your comment'
        else:
            recipient = instance.post.user
            verb = 'create comment on your post'

        if recipient != actor:
            Notification.objects.create(
                actor=actor,
                recipient=recipient,
                verb=verb,
                target=instance.post 
            )

@receiver(post_save, sender=Like)
def send_notification_after_save_like(sender, instance, created, **kwargs):
    if created:
        actor = instance.user
        recipient = instance.post.user

        if recipient != actor:
            Notification.objects.create(
                actor=actor,
                recipient=recipient,
                verb='liked your post',
                target=instance.post
            )

@receiver(post_save, sender=Share)
def send_notification_after_save_share(sender, instance, created, **kwargs):
    if created:
        actor = instance.user
        recipient = instance.post.user

        if recipient != actor:
            Notification.objects.create(
                actor=actor,
                recipient=recipient,
                verb='shared your post',
                target=instance.post
            )