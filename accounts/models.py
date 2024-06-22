from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from utils.data import country_phone_codes
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from datetime import timedelta
from django.conf import settings

class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_email_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_email_verified") is not True:
            raise ValueError("Superuser must have is_email_verified=True.")

        return self._create_user(username, email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    user_type_choices = [("NO", "normal"), ("RO", "restaurant owner")]
    gender_choices = [('M', "male"), ("F", "female"), ("O", "other")]

    email = models.EmailField(unique=True)
    user_type = models.CharField(choices=user_type_choices, max_length=5, default="NO")
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    phone_country_code = models.CharField(default="+91", choices=country_phone_codes, max_length=10)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="images/accounts", default="images/accounts/default.png")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=gender_choices, blank=True, max_length=1)
    biography = models.TextField(blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username' # this field will always unique. can be email or username or other unique fields
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
class OTP(models.Model):

    type_Of_otp_choices = [("email", "E"), ("phone", "P")]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_Of_otp = models.CharField(max_length=10, choices=type_Of_otp_choices)
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expiring_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=settings.OTP_VALIDITY_MINUTES))
    def __str__(self):
        return f"{self.user} - {self.type_Of_otp} - {self.otp}"
        
    def is_otp_expired(self):
        return timezone.now() > self.expiring_at
    
    def send_otp_via_email(self, email, otp):
        company_name = "Restaurant Lookup"
        subject, from_email, to = "E-mail Verification", settings.EMAIL_HOST_USER, email
        text_content = "This is an important message."
        html_content = f"""
            <p>Hi User,</p>
            <p>Welcome to {company_name}</p>
            <p>To complete your registration and verify your email address, please use the following One-Time Password (OTP):</p>
            <div class="otp-code" style="font-size: 24px; font-weight: bold;">
                {otp}
            </div>
            <p>This code is valid for the next 15 minutes. Please enter it in the required field to complete your verification process.</p>
            <p>If you did not request this email, please ignore it. For security purposes, do not share this code with anyone.</p>
            <p>Thank you for joining {company_name}</p>
            <p>Best regards,<br>The {company_name} Team</p>
        """
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.content_subtype = "html"
        msg.send()