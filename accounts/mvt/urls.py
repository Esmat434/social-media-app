from django.urls import path

from .views import (
    RegisterView,LoginView,LogoutView,ProfileView,ProfileUpdateView,AccountVerifiedView,
    CreateChangePasswordTokenView,ChangePasswordView,CreateForgotPasswordTokenView,
    ForgotPasswordView
)

app_name = 'accounts'

urlpatterns = [
    # MVT Part
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/update/',ProfileUpdateView.as_view(),name='profile_update'),
    path('account_verified/<uuid:uuid>/',AccountVerifiedView.as_view(),name='account_verified'),
    path('create_change_password_token/',CreateChangePasswordTokenView.as_view(),name='create_change_password_token'),
    path('change_password/<uuid:uuid>/',ChangePasswordView.as_view(),name='change_password'),
    path('create_forgot_password_token/',CreateForgotPasswordTokenView.as_view(),name='create_forgot_password_token'),
    path('forgot_password/<uuid:uuid>/',ForgotPasswordView.as_view(),name='forgot_password')
]
