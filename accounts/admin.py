from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Extra Information",
            {
                "fields": (
                    ("user_type", "gender"),
                    ("is_email_verified", 
                    "is_phone_verified", ),
                    ("phone_country_code", 
                    "phone", ),
                    "profile_picture_url", 
                    "date_of_birth", 
                    "biography"
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None, 
            {
                "classes": ("wide",), 
                "fields": ("username", "email", "password1", "password2")
            }
        ),
    )
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser

    list_display = ["username", "email", "first_name", "last_name", "user_type", "is_email_verified", "is_phone_verified"]