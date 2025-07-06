import pytest

from accounts.models import (
    CustomUser
)

from accounts.mvt.forms import (
    UserForm,UserUpdateForm,ChangePasswordForm,ForgotPasswordTokenForm,ForgotPasswordForm
)

@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
            username='test',email='test@gmail.com',address='Timany',city='Kabul',country='AF',
            )

@pytest.mark.django_db
def test_user_form_validate():
    data = {
        'username':'test','email':'test@gmail.com','address':'Timany','city':'Kabul','country':'AF',
        'birth_date':'2000-01-02','password':'Test12345%','password1':'Test12345%'
    }
    form = UserForm(data=data)
    assert form.is_valid() == True

@pytest.mark.django_db
def test_update_user_form_validate(user):
    data = {
        'username':'change','email':'change@gmail.com','address':'Timany','city':'Kabul',
        'country':'AF','birth_date':'2000-03-01'
    }
    form = UserUpdateForm(data=data,instance=user)
    print(form.errors)
    assert form.is_valid() == True

def test_change_password_form():
    data = {
        'password1':'Test12345%','password2':'Test12345%'
    }
    form = ChangePasswordForm(data=data)
    assert form.is_valid() == True

def test_forgot_password_token_form(user):
    data = {
        'email':'test@gmail.com'
    }
    form = ForgotPasswordTokenForm(data=data)
    assert form.is_valid() == True

def test_forgot_password_form():
    data = {
        'password1':'Test12345%',
        'password2':'Test12345%'
    }
    form = ForgotPasswordForm(data=data)
    assert form.is_valid() == True