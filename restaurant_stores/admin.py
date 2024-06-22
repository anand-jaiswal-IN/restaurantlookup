from django.contrib import admin
from .models import Address, Restaurant, RestaurantImages, Food_category, Subfood_category, Dish

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'state', 'postal_code', 'user']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'user', 'is_verified']

@admin.register(RestaurantImages)
class RestaurantImagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'restaurant']
    
@admin.register(Food_category)
class Food_CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Subfood_category)
class Subfood_categoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description']

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_sub_category','is_verified']

    def get_sub_category(self, obj):
        return ", ".join([sub_category.name for sub_category in obj.sub_category.all()])
    get_sub_category.short_description = "Sub Category"