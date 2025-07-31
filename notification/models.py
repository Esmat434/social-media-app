from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    """
    مدلی برای ذخیره کردن تمام اعلان‌های سیستم.
    """
    # ۱. گیرنده اعلان (کاربری که اعلان را می‌بیند)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    
    # ۲. فاعل (کاربری که عمل را انجام داده است)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='actions'
    )
    
    # ۳. فعل (متنی که عمل را توصیف می‌کند)
    # مثال: "پست شما را لایک کرد", "برای شما درخواست دوستی فرستاد"
    verb = models.CharField(max_length=255)
    
    # ۴. وضعیت خوانده شده (برای مدیریت اعلان‌های جدید)
    is_read = models.BooleanField(default=False, db_index=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    # --- بخش کلیدی: لینک به آبجکت هدف ---
    # این سه فیلد با هم کار می‌کنند تا به هر آبجکتی لینک دهند
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        if self.target:
            return f'{self.actor.username} {self.verb} on {self.target}'
        return f'{self.actor.username} {self.verb}'