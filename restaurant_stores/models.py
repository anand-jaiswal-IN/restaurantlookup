from django.db import models
from accounts.models import CustomUser as User
from utils.data import countries, states_list

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Address (TimeStampedModel):
    street = models.CharField(max_length=50)
    appratment_number = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(choices=states_list, max_length=5, default="IN_UP")
    postal_code = models.IntegerField()
    country = models.IntegerField(choices=countries, default=76)
    landmark = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.IntegerField(null=True, blank=True)
    longitude = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.appratment_number}, {self.street}, {self.city}, {self.state[3:]}, Pin-Code: {self.postal_code}'

class Restaurant(TimeStampedModel):
    name = models.CharField(max_length=50)
    logo_url = models.URLField(default="https://res.cloudinary.com/dgzc1nbnk/image/upload/v1719569947/ce7cbrs6xdwezeurgxzz.jpg")
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, unique=True)
    website = models.URLField(max_length=50, default="https://www.yourdomain.com")
    description = models.TextField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opening_hours_from = models.TimeField(null=True, blank=True)
    opening_hours_to = models.TimeField(null=True, blank=True)
    is_open_now = models.BooleanField(default=False)
    reason_for_not_opening = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
class RestaurantImages(TimeStampedModel):
    image_url = models.URLField()
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.restaurant.user}{self.restaurant.name}'
    
class Food_category (models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="food_category", blank=True, null=True, default="food_category/default.png")
    description = models.TextField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Subfood_category (models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Food_category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="subfood_category", blank=True, null=True, default="subfood_category/default.png")
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Dish(TimeStampedModel):
    name = models.CharField(max_length=50)
    image_url = models.URLField()
    price = models.IntegerField()
    sub_category = models.ManyToManyField(Subfood_category)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name