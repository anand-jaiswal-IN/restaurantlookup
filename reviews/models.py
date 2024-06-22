from typing import Any
from django.db import models
from accounts.models import CustomUser as User
from utils.data import rating_nums
from restaurant_stores.models import Restaurant, Dish
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ReviewToken(TimeStampedModel):
    token = models.CharField(max_length=100)
    type_of_review = models.CharField(choices=[("R", "restaurant"), ("D", "dish")], max_length=1)
    which_restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    which_dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True, blank=True)
    for_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type_of_review} for {self.user.username}'

    def generateToken(self):
        from django.utils.crypto import get_random_string
        self.token = get_random_string(length=25)
        self.save()

    def send_token_via_email(self):
        company_name = "Restaurant Lookup"
        subject, from_email, to = f"Feedback!", settings.EMAIL_HOST_USER, self.for_user.email
        text_content = "This is an important message."
        html_content = f"""
            <p>Hi User,</p>
            <p>Welcome to {company_name}</p>
            <p>We Value Your Feedback! Enjoy a Complimentary Token from {company_name}</p>
            <div class="otp-code" style="font-size: 24px; font-weight: bold;">
                <p> Token = {self.token} </p>
            </div>
            <p><a href="/feedback/{self.type_of_review}/{self.pk}/">Click here</a> to submit your review.</p>
            <p>Your insights will help us enhance our services and ensure that we continue to delight our guests. To redeem your complimentary token, simply present this email to our staff during your next visit.</p>
            <p>Thank you for your support and for taking the time to share your thoughts. We look forward to welcoming you back to {company_name} soon!</p>
            <p>Best regards,<br>The {company_name} Team</p>
        """
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.content_subtype = "html"
        msg.send()

    def save(self, *args, **kwargs):
        if not self.token:
            self.generateToken()
        super().save(*args, **kwargs)
    
class RatingRestaurant(TimeStampedModel):
    which = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, null=True, blank=True)
    rating_number = models.IntegerField(choices=rating_nums)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'To "{self.which.name}" By "{self.user.username}"'
    
class RatingDish(TimeStampedModel):
    which = models.ForeignKey(Dish, on_delete=models.CASCADE)
    description = models.TextField(max_length=100, null=True, blank=True)
    rating_number = models.IntegerField(choices=rating_nums)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'To "{self.which.name}" By "{self.user.username}"'