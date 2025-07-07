from rest_framework import serializers

from django.contrib.auth import authenticate,login

from utils.validate import (
    validate_birth_date,validate_password
)
from accounts.models import (
    CustomUser,AccountVerificationToken,ChangePasswordToken,ForgotPasswordToken
)

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    avatar = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    password2 = serializers.CharField(max_length=128,required=True,write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username','email','first_name','last_name','avatar','phone_number','address',
            'city','country','birth_date','password','password2'
        )
    
    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validate_data):
        validate_data.pop('password2')
        password = validate_data.pop("password",None)
        
        for key,value in validate_data.items():
            setattr(instance,key,value)
        
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_username(self,value):
        if CustomUser.objects.filter(username = value).exists():
            raise serializers.ValidationError("This username already exists.")
        return value
    
    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value
    
    def validate_birth_date(self,value):
        status = validate_birth_date(value)

        if not status:
            raise serializers.ValidationError("Your age must be at least 18+")
        return value
    
    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError("Passwords do not match.")
            
            status = validate_password(password1)
            if not status:
                raise serializers.ValidationError("Your password must contain  a-zA-Z1-9!@#$%^&*")
        return attrs

class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    avatar = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    
    class Meta:
        model = CustomUser
        fields = (
            'username','email','first_name','last_name','avatar','phone_number','address',
            'city','country','birth_date','password'
        )
    
    def update(self, instance, validate_data):
        password = validate_data.pop("password",None)
        
        for key,value in validate_data.items():
            setattr(instance,key,value)
        
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_username(self,value):
        if CustomUser.objects.filter(username = value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("This username already exists.")
        return value
    
    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("This email already exists.")
        return value
    
    def validate_birth_date(self,value):
        status = validate_birth_date(value)

        if not status:
            raise serializers.ValidationError("Your age must be at least 18+")
        return value
    
    def validate(self, attrs):
        password1 = attrs.get('password',None)

        if password1:
            status = validate_password(password1)
            if not status:
                raise serializers.ValidationError("Your password must contain  a-zA-Z1-9!@#$%^&*")
        return attrs

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(username = username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("You don’t have an account.")
        if not user.email_verified:
            raise serializers.ValidationError("Your account is not active.")
        
        if not password:
            raise serializers.ValidationError("Please enter your password.")
        
        if not validate_password(password):
            raise serializers.ValidationError("Your password must contain a-zA-Z0-9!@#$%^&*")

        return data

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def save(self, user):
        user.set_password(self.validated_data['password'])
        user.save()

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
    
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        if not validate_password(password):
            raise serializers.ValidationError("Password must include a-z, A-Z, 0-9 and special characters like !@#$%^&*.")
        
        return data

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not CustomUser.objects.filter(email=email).first():
            raise serializers.ValidationError("You don’t have an account.")
        
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        if not validate_password(password):
            raise serializers.ValidationError("Password must include a-z, A-Z, 0-9 and special characters like !@#$%^&*.")
        
        return data
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = CustomUser.objects.get(email=email)
        user.set_password(password)
        user.save()
        return user
