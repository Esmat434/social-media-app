from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,AccountVerificationToken,ChangePasswordToken,ForgotPasswordToken
)

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "avatar", "address", 
                                      "city", "country", "birth_date",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "email_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "avatar", "address", "city", 
                           "country", "birth_date", "password1", "password2"),
            },
        ),
    )

@admin.register(AccountVerificationToken)
class AccountVerifiedAdmin(admin.ModelAdmin):
    list_display = ['id','user','token','created_at','expires_at']

@admin.register(ChangePasswordToken)
class ChangePasswordAdmin(admin.ModelAdmin):
    list_display = ['id','user','token','created_at','expires_at']

@admin.register(ForgotPasswordToken)
class ForgotPasswordAdmin(admin.ModelAdmin):
    list_display = ['id','user','token','created_at','expires_at']