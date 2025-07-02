from django import forms
from django.contrib.auth import get_user_model
from django_countries.widgets import CountrySelectWidget

from utils.validate import (
    validate_password,validate_birth_date,validate_phone_number
)

from accounts.models import (
    CustomUser
)

User = get_user_model()

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Confirmation Password'})
        )
    class Meta:
        model = CustomUser
        fields = (
            'username','email','first_name','last_name','avatar','phone_number',
            'address','city','country','birth_date','password','password1'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter User Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'avatar': forms.FileInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Phone Number'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Address'}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter City'}),
            'country': CountrySelectWidget(attrs={'class':'form-control'}),
            'birth_date': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Enter Birth Date'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Confirmation Password'})
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("This username is already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("This email is already exists")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number","")

        if phone_number:
            status = validate_phone_number(phone_number)
            if not status:
                raise forms.ValidationError("Your phone number is not correct your number must contain country code and be correct.")
            return phone_number
        return phone_number
        
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']

        status = validate_birth_date(birth_date)
        if not status:
            raise forms.ValidationError("your age at least 18+")
        return birth_date
    
    def clean(self):
        cleaned_data =  super().clean()

        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password1')
        
        if not password1 or not password2:
            raise forms.ValidationError("Your must set your password")

        if password1 != password2:
            raise forms.ValidationError("Your password must be same with confirmation password")
        
        status = validate_password(password1)
        if not status:
            raise forms.ValidationError("your password must be contain one upper case one lower case letter and one digit and one !@#$%^&*")
        
        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'username','email','first_name','last_name','avatar','phone_number',
            'address','city','country','birth_date'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter User Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'avatar': forms.FileInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Phone Number'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Address'}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter City'}),
            'country': CountrySelectWidget(attrs={'class':'form-control'}),
            'birth_date': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Enter Birth Date'}),
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username = username).exclude(pk = self.instance.pk).exists():
            raise forms.ValidationError("This username is already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email = email).exclude(pk = self.instance.pk).exists():
            raise forms.ValidationError("This email is already exists")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number","")

        if phone_number:
            status = validate_phone_number(phone_number)
            if not status:
                raise forms.ValidationError("Your phone number is not correct your number must contain country code and be correct.")
            return phone_number
        return phone_number
        
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']

        status = validate_birth_date(birth_date)
        if not status:
            raise forms.ValidationError("your age at least 18+")
        return birth_date

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Password'})
    )
    password2 = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Confirmation Password.'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError("Your password must be same with confirmation password.")
        
        status = validate_password(password1)
        
        if not status:
            raise forms.ValidationError("Your password must be contain one upper case one lower case letter and one digit and one !@#$%^&*")

        return cleaned_data

class ForgotPasswordTokenForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean(self):
        validate = super().clean()

        email = validate['email']

        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Your dont't have and account.")
        
        return validate

class ForgotPasswordForm(forms.Form):
    password1 = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Password'})
    )
    password2 = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Confirmation Password.'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError("Your password must be same with confirmation password.")
        
        status = validate_password(password1)
        
        if not status:
            raise forms.ValidationError("Your password must be contain one upper case one lower case letter and one digit and one !@#$%^&*")

        return cleaned_data