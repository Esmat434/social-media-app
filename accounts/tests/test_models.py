import pytest
from accounts.models import (
    CustomUser,AccountVerificationToken,ChangePasswordToken,ForgotPasswordToken
)

@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
            username='test',email='test@gmail.com',address='Timany',city='Kabul',country='AF',
            )

@pytest.fixture
def account_verified_token(user):
    return AccountVerificationToken.objects.create(user=user)

@pytest.fixture
def change_password_token(user):
    return ChangePasswordToken.objects.create(user=user)

@pytest.fixture
def forgot_password_token(user):
    return ForgotPasswordToken.objects.create(user=user)


def test_customuser_model(user):
    assert user.username == 'test'
    assert user.email == 'test@gmail.com'
    assert user.address == 'Timany'

def test_account_verification_token_model(account_verified_token):
    assert account_verified_token.user.username == 'test'

def test_change_password_token_model(change_password_token):
    assert change_password_token.user.username == 'test'

def test_forgot_password_token_model(forgot_password_token):
    assert forgot_password_token.user.username == 'test'