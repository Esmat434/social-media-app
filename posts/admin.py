from django.contrib import admin

from .models import (
    Post,PostMedia,Like,Comment,Share,Save
)

class PostMediaAdmin(admin.TabularInline):
    model = PostMedia
    extra = 1

class CommentAdmin(admin.StackedInline):
    model = Comment
    fields = (
        'user','parent','comment'
    )
    readonly_fields = ('user',)
    extra = 1

class LikeAdmin(admin.TabularInline):
    model = Like
    readonly_fields = ('user',)
    extra = 0

class ShareAdmin(admin.TabularInline):    
    model = Share
    readonly_fields = ('user',)
    extra = 0

class SaveAdmin(admin.TabularInline):    
    model = Save
    readonly_fields = ('user',)
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user','published_at','created_at','updated_at']
    search_fields = ['content','user__username']
    list_filter = ['user','published_at','created_at','updated_at']
    inlines = (
        PostMediaAdmin,
        CommentAdmin,
        LikeAdmin,
        ShareAdmin,
        SaveAdmin
    )
