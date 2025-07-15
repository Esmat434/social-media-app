import pytest

from django.contrib.auth import get_user_model

from accounts.api.serializers import (
    UserSerializer,UpdateUserSerializer,LoginSerializer,ChangePasswordSerializer,
    ForgotPasswordSerializer
)

User = get_user_model()

@pytest.fixture
def user(db):
    password = 'Test12345%'
    user = User.objects.create_user(
            username='test',email='test@gmail.com',address='Timany',city='Kabul',country='AF',
            email_verified=True,password=password
            )
    user.raw_password = password
    return user

@pytest.mark.django_db
class TestUserSerializer:

    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user

    def test_create_user_serializer(self):
        data = {
            'username':'tester','email':'tester@gmail.com','first_name':'test','last_name':'test',
            'address':'timani','city':'kabul','country':'AF','birth_date':'2000-01-02',
            'password':'Test12345%','password2':'Test12345%'
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid() == True
    
    def test_update_user_serializer(self):
        partial_data = {
            'username':'Change','email':'Change@gmail.com'
        }
        serializer = UserSerializer(instance=self.user,data=partial_data,partial=True)

        assert serializer.is_valid() == True

class TestUpdateUserSerializer:
    
    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user

    def test_update_user_serializer(self):
        data = {
            'username':'ali','email':'ali@gmail.com'
        }
        serializer = UpdateUserSerializer(instance=self.user, data=data, partial=True)
        
        assert serializer.is_valid() == True
    
class TestLoginSerializer:

    @pytest.fixture(autouse=True)
    def setUp(self,user):
        self.user = user
    
    def test_login_serializer(self):
        data = {
            'username':self.user.username,
            'password':self.user.raw_password
        }
        serializer = LoginSerializer(data=data)

        assert serializer.is_valid() == True

class TestChangePasswordSerializer:
    
    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.client = client
        self.user = user
        self.client.force_login(self.user)
    
    def test_change_password_serializer(self):
        data = {
            'password':'Test12345%',
            'confirm_password':'Test12345%'
        }
        serializer = ChangePasswordSerializer(data=data)

        assert serializer.is_valid() == True

class TestForgotPasswordSerializer:

    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.client = client
        self.user = user
    
    def test_forgot_password_serializer(self):
        data = {
            'email':self.user.email,
            'password':'Test12345%',
            'confirm_password':'Test12345%'
        }
        serializer = ForgotPasswordSerializer(data=data)

        assert serializer.is_valid() == True
