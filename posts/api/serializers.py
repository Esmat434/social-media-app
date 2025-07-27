from rest_framework import serializers

from posts.algorithms.validators import word_filtering

from posts.models import (
    Post,PostMedia,Like,Share,Save,Comment
)

class PostMediaSerializer(serializers.ModelSerializer):
    VIDEO_TYPES = ['mp4','mkv','avi','webm']
    IMAGE_TYPES = ['jpg','jpeg','png','gif','svg']
    class Meta:
        model = PostMedia
        fields = ['file']
    
    def get_file_type(self,file):
        extension = file.name.split('.')[-1].lower()
        is_image = extension in self.IMAGE_TYPES
        is_video = extension in self.VIDEO_TYPES

        return is_image,is_video        

    def validate_file(self,value):
        IMAGE_MAX_SIZE = 5 * 1024 * 1024
        VIDEO_MAX_SIZE = 50 * 1024 * 1024

    
        is_image, is_video = self.get_file_type(value)  

        if not (is_image or is_video):
            raise serializers.ValidationError("Only images and videos are supported.")
        
        if is_image and value.size > IMAGE_MAX_SIZE:
            raise serializers.ValidationError("Your image size must be less than 5 MB.")
        
        if is_video and value.size > VIDEO_MAX_SIZE:
            raise serializers.ValidationError("Your video size must be less than 50 MB.")
        
        return value

class PostSerializer(serializers.ModelSerializer):
    VIDEO_TYPES = ['mp4','mkv','avi','webm']
    IMAGE_TYPES = ['jpg','jpeg','png','gif','svg']
    media = PostMediaSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'content', 'media')
    
    def validate_content(self,value):
        status_text = word_filtering(value)
        if status_text == True:
            raise serializers.ValidationError('Your content is not legal and politness.')
        return value

    def get_file_type(self,file):
        extension = file.name.split('.')[-1].lower()
        is_image = extension in self.IMAGE_TYPES
        is_video = extension in self.VIDEO_TYPES

        return is_image,is_video
    
    def create(self, validated_data):
        media_data = validated_data.pop('media', [])
        post = Post.objects.create(**validated_data)

        for media_dict in media_data:
            file = media_dict.get('file')
            is_image, is_video = self.get_file_type(file)
            media_type = 'image' if is_image else 'video' if is_video else 'Unknown'
            PostMedia.objects.create(post=post, file=file, media_type=media_type)
        return post
    
    def update(self, instance, validated_data):
        media_data = validated_data.pop('media', [])

        for key,value in validated_data.items():
            setattr(instance,key,value)


        if media_data:
            PostMedia.objects.filter(post=instance).delete()
            for media_dict in media_data:
                file = media_dict.get('file')
                is_image,is_video = self.get_file_type(file)
                media_type = 'image' if is_image else 'video' if is_video else 'Unknown'
                PostMedia.objects.create(post=instance, file=file, media_type=media_type)        
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id','post','parent','comment'
        )
        extra_kwargs = {
            'id':{'read_only':True},
            'post':{'write_only':True}
        }
    
    def validate_comment(self,value):
        status_text = word_filtering(value)
        if status_text:
            raise serializers.ValidationError('Your comment is not legal and politness.')
        
        return value

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'id','post','status'
        )
        extra_kwargs = {
            'post':{'write_only':True}
        }

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = (
            'id','post','status'
        )
        extra_kwargs = {
            'post':{'write_only':True}
        }

class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = (
            'id','post','status'
        )
        extra_kwargs = {
            'post':{'write_only':True}
        }
