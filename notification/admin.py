from django.contrib import admin
from .models import Notification
# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id','recipient','actor','verb','is_read','content_type','object_id','target']