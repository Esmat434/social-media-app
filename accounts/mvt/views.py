import uuid
from datetime import timedelta
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseNotFound
from django.urls import reverse,reverse_lazy
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.views.generic.edit import FormView
from django.views import View
from django.views.generic import (
    DetailView,CreateView,UpdateView
)

from .email import send_verification_mail

from .mixins import (
    LoginRequiredMixin,LogoutRequiredMixin,AccountVerifiedBeforeLoginMixin
)

from accounts.models import (
    CustomUser,AccountVerificationToken,ChangePasswordToken,ForgotPasswordToken
)
from .forms import (
    UserForm,UserUpdateForm,ChangePasswordForm,ForgotPasswordTokenForm,ForgotPasswordForm,
    CreateAccountVerifiedTokenForm
)

class RegisterView(LogoutRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'accounts/register_form.html'
    context_object_name = 'form'

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = form.save()

                token_instance = AccountVerificationToken.objects.create(user=user)

                domain = getattr(settings, 'SITE_DOMAIN', 'http://localhost:8000')
                link = domain + reverse('mvt:account_verified', args=[token_instance.token])

                send_verification_mail(
                    token_instance.user.email,
                    'Account Activation Token',
                    token_instance.user.username,
                    link
                )
        except Exception as e:
            form.add_error(None, 'ثبت‌نام با خطا مواجه شد. لطفاً دوباره تلاش کنید.')
            return self.form_invalid(form)

        return render(self.request, 'accounts/register_success.html', {'user': user})

class LoginView(AccountVerifiedBeforeLoginMixin,LogoutRequiredMixin,View):
    def get(self,request):
        return render(request,'accounts/login.html')
    
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request,user)
            messages.success(request,"you successfully logged in.")
            return redirect('/')
        else:
            messages.error(request,'Your username or password is incorrect.')
            return render(request,'accounnts/login.html')

class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'accounts/logout.html')
    
    def post(self,request):
        logout(request)
        return redirect('/')

class ProfileView(LoginRequiredMixin,DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset = ...):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'accounts/profile_update.html'    
    context_object_name = 'form'
    success_url = reverse_lazy('mvt:profile')

    def get_object(self, queryset = ...):
        return self.request.user

class CreateAccountVerifiedTokenView(LogoutRequiredMixin,FormView):
    form_class = CreateAccountVerifiedTokenForm
    template_name = 'accounts/create_account_verify_token.html'
    
    def form_valid(self, form):
        email = form.cleaned_data['email']

        user = CustomUser.objects.get(email=email)

        new_token_val = uuid.uuid4()
        new_expiry_val = timezone.now() + timedelta(hours=24)

        avt_token,created = AccountVerificationToken.objects.update_or_create(
            user = user,
            defaults={
                'token':new_token_val,
                'expires_at':new_expiry_val
            }
        )

        domain = getattr(settings, 'SITE_DOMAIN', 'http://localhost:8000')
        link = domain + reverse('mvt:account_verified', args=[avt_token.token])

        send_verification_mail(
            avt_token.user.email,
            'Account Activation Token',
            avt_token.user.username,
            link
        )

        return render(self.request,'accounts/register_success.html')


class AccountVerifiedView(LogoutRequiredMixin,View):
    def get(self, request,uuid):
        token_val = uuid
        token_obj = get_object_or_404(AccountVerificationToken, token=token_val)

        if token_obj.is_expired():
            return HttpResponseNotFound("Your tokne is expired.")
        
        self.user = token_obj.user
        self.user.email_verified = True
        self.user.save()
        token_obj.delete()

        return redirect('mvt:login')

class CreateChangePasswordTokenView(LoginRequiredMixin,View):
    def post(self, request):
        username = request.user.username
        user = get_object_or_404(CustomUser, username=username)

        new_token_val = uuid.uuid4()
        new_expiry_val = timezone.now() + timedelta(hours=24)

        # ایجاد توکن برای تغییر رمز عبور
        cpt_obj,created = ChangePasswordToken.objects.update_or_create(
            user=user,
            defaults={
                'token': new_token_val,
                'expires_at': new_expiry_val
            }
        )

        # ساخت لینک
        domain = getattr(settings, 'SITE_DOMAIN', 'http://localhost:8000')
        link = domain + reverse('mvt:change_password', args=[cpt_obj.token])

        # ارسال ایمیل
        send_verification_mail(
            to=user.email,
            subject='Change Password Token',
            username=user.username,
            link=link
        )

        return render(request, 'accounts/change_password_message.html')


class ChangePasswordView(LoginRequiredMixin,FormView):
    form_class = ChangePasswordForm
    template_name = 'accounts/change_password.html'
    context_object_name = 'form'
    success_url = reverse_lazy('mvt:profile')

    def dispatch(self, request, *args, **kwargs):
        self.token = self.kwargs['uuid']
        self.token_obj = get_object_or_404(ChangePasswordToken, token=self.token)

        if self.token_obj.is_expired():
            return HttpResponseNotFound("Your token is expired.")
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        password = form.cleaned_data['password1']
        user = self.request.user
        user.set_password(password)
        user.save()

        ChangePasswordToken.objects.filter(user=user).first().delete()

        update_session_auth_hash(self.request,user)

        return super().form_valid(form)

class CreateForgotPasswordTokenView(LogoutRequiredMixin,FormView):
    form_class = ForgotPasswordTokenForm
    template_name = 'accounts/create_forgot_password_token.html'
    
    def form_valid(self, form):
        email = form.cleaned_data['email']

        user = CustomUser.objects.get(email=email)

        new_token_val = uuid.uuid4()
        new_expiry_at = timezone.now() + timedelta(hours=24)

        fpt_obj,created = ForgotPasswordToken.objects.update_or_create(
            user=user,
            defaults={
                'token': new_token_val,
                'expires_at': new_expiry_at
            }
        )

        domain = getattr(settings,'SITE_DOMAIN','http://localhost:8000')
        link = domain + reverse('mvt:forgot_password', args=[fpt_obj.token])
        send_verification_mail(
            fpt_obj.user.email,
            'Forgot Password Token.',
            fpt_obj.user.username,link
        )

        return render(self.request,'accounts/forgot_password_token_message.html',{'email':user.email})

class ForgotPasswordView(LogoutRequiredMixin,FormView):
    form_class = ForgotPasswordForm
    template_name = 'accounts/forgot_password.html'
    success_url = reverse_lazy('mvt:login')

    def dispatch(self, request, *args, **kwargs):
        self.token_value = self.kwargs.get('uuid')
        self.token_obj = get_object_or_404(ForgotPasswordToken, token=self.token_value)

        if self.token_obj.is_expired():
            return HttpResponseNotFound("Your token is expired.")
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['password1']

        user=self.token_obj.user
        user.set_password(password)
        user.save()

        self.token_obj.delete()

        return super().form_valid(form)