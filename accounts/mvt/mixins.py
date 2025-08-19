from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('mvt:login'))
        return super().dispatch(request,*args,**kwargs)

class LogoutRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request,*args,**kwargs)

class AccountVerifiedBeforeLoginMixin:
    def dispatch(self,request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'Your username or password is not correct.')
                return render(request, 'accounts/login.html')

            if not getattr(user,'email_verified',False):
                messages.error(request, 'Please verify your email before logging in.')
                return render(request, 'accounts/account_verified_message.html')
            
        return super().dispatch(request,*args,**kwargs)