from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = "__all__"

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "user_type", "date_of_birth", "gender", "biography", ]

class ChangeUsernameForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class ChangePasswordForm(forms.ModelForm):
    
    old_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['password']

class ChangeEmailForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password']