from . import views 
from django.urls import path

app_name = 'restaurant_stores'

urlpatterns = [
    path('', view=views.home, name='home'),
    path('restaurant_stores/', view=views.restaurant_stores, name='restaurant_stores'),
    path('store/<int:restaurant_id>/', view=views.store, name='store'),


    path('your_restaurant/<int:restaurant_id>/', view=views.your_restaurant, name='your_restaurant'),
    path('add_restaurant/', view=views.add_restaurant, name='add_restaurant'),
    path('add_address/', view=views.add_address, name='add_address'),

    path('delete_restaurant/', view=views.delete_restaurant, name="delete_restaurant"),
    path('delete_restaurant_dish/', view=views.delete_restaurant_dish, name="delete_restaurant_dish"),
    path('delete_restaurant_image/', view=views.delete_restaurant_image, name="delete_restaurant_image"),

    path('update_restaurant_logo/<int:restaurant_id>', view=views.update_restaurant_logo, name='update_restaurant_logo'),

    path('add_restaurant_dish/<int:restaurant_id>/', view=views.add_restaurant_dish, name="add_restaurant_dish"),
    path('add_restaurant_image/<int:restaurant_id>/', view=views.add_restaurant_image, name="add_restaurant_image"),

    path('dish/<int:dish_id>/', view=views.dish, name="dish"),
]
