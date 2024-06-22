from django.contrib import admin
from .models import RatingDish, RatingRestaurant

@admin.register(RatingRestaurant)
class Rating_restaurantAdmin(admin.ModelAdmin):
    list_display = ['which', 'description', 'rating_number', 'user']

@admin.register(RatingDish)
class Rating_dishAdmin(admin.ModelAdmin):
    list_display = ['which', 'description', 'rating_number', 'user']