from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView
)
from .views import (
    RegisterView,LoginView,LogoutView,ProfileView,ChangePasswordView,ForgotPasswordView
)

app_name = 'accounts'

urlpattern = [
    # API JWT Part
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom API Part
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('change_password/<uuid:uuid>/',ChangePasswordView.as_view(),name='change_password'),
    path('forgot_password/<uuid:uuid>/',ForgotPasswordView.as_view(),name='forgot_password'),

]