import pytest

from django.urls import reverse

from accounts.models import (
    CustomUser,AccountVerificationToken,ChangePasswordToken,ForgotPasswordToken
)

@pytest.fixture
def user(db):
    password = 'Test12345%'
    user = CustomUser.objects.create_user(
            username='test',email='test@gmail.com',address='Timany',city='Kabul',country='AF',
            email_verified=True,password=password
            )
    user.raw_password = password
    return user

@pytest.mark.django_db
class TestRegisterView:
    def test_get_method_register_view(self,client):
        url = reverse('mvt:register')
        response = client.get(url)

        assert response.status_code == 200
        assert 'accounts/register_form.html' in [t.name for t in response.templates]
    
    def test_post_method_register_view(self,client):
        url = reverse('mvt:register')
        data = {
            'username':'test','email':'test@gmail.com','address':'Timany','city':'Kabul','country':'AF',
            'birth_date':'2000-01-02','email_verified':True,'password':'Test12345%','password1':'Test12345%'
        }
        response = client.post(url,data)
        print()
        assert response.status_code == 200
        assert 'accounts/register_success.html' in [t.name for t in response.templates]

class TestLoginView:
    def test_get_method_login_view(self,client):
        url = reverse('mvt:login')
        response = client.get(url)

        assert response.status_code == 200
        assert 'accounts/login.html' in [t.name for t in response.templates]
    
    def test_post_method_login_view(self,user,client):
        url = reverse('mvt:login')
        data = {
            'username':user.username,
            'password':user.raw_password
        }
        response = client.post(url,data)

        assert response.status_code == 302
        assert response.url == '/'

class TestLogoutView:
    def test_post_method_logout_view(self,user,client):
        client.force_login(user)
        url = reverse('mvt:logout')
        response = client.post(url)

        assert response.status_code == 302
        assert response.url == '/'

class TestProfileView:
    def test_profile_view(self,user,client):
        client.force_login(user)
        url = reverse('mvt:profile', args=[user.username])
        response = client.get(url)

        assert response.status_code == 200
        assert 'accounts/profile.html' in [t.name for t in response.templates]

class TestProfileUpdateView:

    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.client = client
        self.user = user
        self.client.force_login(self.user)

    def test_get_method_profile_update_view(self):
        url = reverse('mvt:profile_update')
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'accounts/profile_update.html' in [t.name for t in response.templates]
    
    def test_post_method_profile_update_view(self):
        url = reverse('mvt:profile_update')
        data = {
            'username':'change','email':'change@gmail.com','address':'timani','city':'kabul',
            'country':'AF','birth_date':'2000-01-02'
        }
        response = self.client.post(url,data)
        assert response.status_code == 302
        assert response.url == reverse('mvt:profile', args=['change'])

class TestAccountVerifiedView:
    
    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.client = client
        self.user = user
        self.token_obj = AccountVerificationToken.objects.create(user=self.user)
    
    def test_get_method_account_verified_view(self):
        url = reverse('mvt:account_verified',args=[self.token_obj.token])
        response = self.client.get(url)

        assert response.status_code == 302
        assert response.url == reverse('mvt:login')

class TestCreateChangePasswordTokenView:
    
    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.user = user
        self.client = client
        self.client.force_login(self.user)
    
    def test_post_method_create_change_password_token_view(self):
        url = reverse('mvt:create_change_password_token')
        response = self.client.post(url)

        assert response.status_code == 200
        assert 'accounts/change_password_message.html' in [t.name for t in response.templates]

class TestChangePasswordView:
    
    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.user = user
        self.client = client
        self.client.force_login(self.user)
        self.token_obj = ChangePasswordToken.objects.create(user=self.user)
    
    def test_get_method_change_password(self):
        url = reverse('mvt:change_password', args=[self.token_obj.token])
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'accounts/change_password.html' in [t.name for t in response.templates]
    
    def test_post_method_change_password(self):
        url = reverse('mvt:change_password', args=[self.token_obj.token])
        data = {
            'password1':'Test12345%',
            'password2':'Test12345%',
        }
        response = self.client.post(url,data)

        assert response.status_code == 302
        assert response.url == reverse('mvt:profile', args=[self.user.username])

class TestCreateForgotPasswordTokenView:

    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.client = client
        self.user = user

    def test_get_method_create_forgot_password_token_view(self):
        url = reverse('mvt:create_forgot_password_token')
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'accounts/create_forgot_password_token.html'
    
    def test_post_method_create_forgot_password_token_view(self):
        url = reverse('mvt:create_forgot_password_token')
        data = {
            'email':self.user.email
        }
        resposne = self.client.post(url,data)

        assert resposne.status_code == 200
        assert 'accounts/forgot_password_token_message.html' in [t.name for t in resposne.templates]

class TestForgotPasswordView:

    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.client = client
        self.user = user
        self.token_obj = ForgotPasswordToken.objects.create(user = self.user)
    
    def test_get_method_forgot_password_view(self):
        url = reverse('mvt:forgot_password', args=[self.token_obj.token])
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'accounts/forgot_password.html' in [t.name for t in response.templates]
    
    def test_post_method_forgot_password_view(self):
        url = reverse('mvt:forgot_password', args=[self.token_obj.token])
        data = {
            'password1':'Test12345%',
            'password2':'Test12345%'
        }
        response = self.client.post(url,data)

        assert response.status_code == 302
        assert response.url == reverse('mvt:login')
    