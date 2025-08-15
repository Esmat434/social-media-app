from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView
)
from .views import (
    RegisterAPIView,LoginAPIView,LogoutAPIView,ProfileAPIView,ProfileUpdateAPIView,
    FriendListAPIView,ChangePasswordAPIView,ForgotPasswordAPIView
)

app_name = 'accounts'

urlpatterns = [
    # API JWT Part
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom API Part
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('logout/',LogoutAPIView.as_view(),name='logout'),
    path('profile/<int:pk>/',ProfileAPIView.as_view(),name='profile'),
    path('profile/<int:pk>/update/',ProfileUpdateAPIView.as_view(),name='profile-update'),
    path('friends/', FriendListAPIView.as_view(), name='friends'),
    path('change_password/',ChangePasswordAPIView.as_view(),name='change_password'),
    path('forgot_password/',ForgotPasswordAPIView.as_view(),name='forgot_password'),

]