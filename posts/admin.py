from django.contrib import admin

from .models import (
    Post,Like,Comment,Share,Save
)
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user','published_at','created_at','updated_at']
    search_fields = ['id']
    list_filter = ['user','published_at','created_at','updated_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','parent','created_at']
    search_fields = ['id']
    list_filter = ['user','post','parent','created_at']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','status','created_at']
    search_fields = ['id']
    list_filter = ['user','post','status','created_at']

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','created_at']
    search_fields = ['id']
    list_filter = ['user','post','created_at']

@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','created_at']
    search_fields = ['id']
    list_filter = ['user','post','created_at']