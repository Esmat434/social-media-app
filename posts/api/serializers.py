from rest_framework import serializers

from posts.models import (
    Post,PostMedia,Like,Share,Save,Comment
)

class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['file', 'media_type']

class PostSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True, required=False)

    class Meta:
        model = Post
        
        fields = ('id', 'content', 'media')
    
    def create(self, validated_data):
        media_data = validated_data.pop('media', [])
        
        post = Post.objects.create(**validated_data)
        for media in media_data:
            PostMedia.objects.create(post=post, **media)
        return post
    
    def update(self, instance, validated_data):
        media_data = validated_data.pop('media', None)

        for key,value in validated_data.items():
            setattr(instance,key,value)


        if media_data:
            PostMedia.objects.filter(post=instance).delete()
            for media in media_data:
                PostMedia.objects.create(post=instance, **media)        
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'post','parent','comment'
        )
        extra_kwargs = {
            'post':{'write_only':True}
        }

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'post','status'
        )
        extra_kwargs = {
            'post':{'write_only':True}
        }

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = (
            'post','status'
        )
        extra_kwargs = {
            'post':{'write_only':True}
        }

class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = (
            'post','status'
        )
        extra_kwargs = {
            'post':{'write_only':True}
        }
