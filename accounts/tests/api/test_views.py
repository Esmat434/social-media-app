import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

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

@pytest.fixture
def auth_client(user,client):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return client

@pytest.mark.django_db
class TestRegisterAPIView:

    @pytest.fixture(autouse=True)
    def setUp(self,client):
        self.client = client
    
    def test_register_api_view(self):
        data = {
            'username':'tester','email':'tester@gmail.com','first_name':'test','last_name':'test',
            'address':'timani','city':'kabul','country':'AF','birth_date':'2000-01-02',
            'password':'Test12345%','password2':'Test12345%'
        }
        url = reverse('api:register')
        response = self.client.post(url,data=data)

        assert response.status_code == 201

class TestLoginAPIView:

    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.client = client
        self.user = user

    def test_login_api_view(self):
        data = {
            'username':self.user.username,
            'password':self.user.raw_password
        }
        url = reverse('api:login')
        response = self.client.post(url,data)

        assert response.status_code == 200

class TestLogoutAPIView:

    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
    
    def test_logout_api_view(self):
        data = {
            'refresh':RefreshToken.for_user(self.user)
        }
        url = reverse('api:logout')
        response = self.client.post(url,data)

        assert response.status_code == 205

class TestProfileAPIView:

    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user

    def test_profile_api_view(self):
        url = reverse('api:profile', args=[self.user.id])
        response = self.client.get(url)

        assert response.status_code == 200

# class TestProfileUpdateAPIView:

#     @pytest.fixture(autouse=True)
#     def setUp(self,user,auth_client):
#         self.client=auth_client
#         self.user=user
    
#     def test_profile_update_api_view(self):
#         data = {
#             'username':'change'
#         }
#         url = reverse('api:profile-update', args=[self.user.id])
#         response = self.client.put(url,data)

#         assert response.status_code == 200

class TestChangePasswordAPIView:

    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.client = auth_client
        self.user = user
    
    def test_change_password_api_view(self):
        data = {
            'password':'Change0000%',
            'confirm_password':'Change0000%'
        }
        url = reverse('api:change_password')
        response = self.client.post(url,data)

        assert response.status_code == 200

class TestForgotPasswordAPIView:

    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.client = client
        self.user = user
    
    def test_forgot_password_api_view(self):
        data = {
            'email':self.user.email,
            'password':'Test12345%',
            'confirm_password':'Test12345%'
        }
        url = reverse('api:forgot_password')
        response = self.client.post(url,data)

        assert response.status_code == 200