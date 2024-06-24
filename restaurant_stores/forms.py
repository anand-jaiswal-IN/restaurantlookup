from django import forms
from .models import Restaurant, Address, Dish, RestaurantImages
from .validators import validate_phone

class AddRestaurantForm(forms.ModelForm):
    phone = forms.CharField(validators=[validate_phone])

    class Meta:
        model = Restaurant
        fields = ["name", "image_logo", "address", "phone", "description", "opening_hours_from", "opening_hours_to", ]

class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street", "appratment_number", "city", "state", "postal_code", "country", "landmark"]

class UpdateRestaurantForm(forms.ModelForm):
    class Meta:
        phone = forms.CharField(validators=[validate_phone])
        
        model = Restaurant
        fields = ["website", "description", "opening_hours_from", "opening_hours_to", 'is_open_now', "reason_for_not_opening"]


class RestaurantImageLogoForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["image_logo"]

class AddDishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "image", "price", "description", "sub_category"]

class AddRestaurantImageForm(forms.ModelForm):
    class Meta:
        model = RestaurantImages
        fields = ["image", "name", "description"]