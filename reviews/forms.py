from django import forms
from .models import ReviewToken, RatingRestaurant, RatingDish
from .models import Restaurant, Dish

class AddReviewTokenForm(forms.ModelForm):

    which_restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all())
    which_dish = forms.ModelChoiceField(queryset=Dish.objects.all(), required=False)

    class Meta:
        model = ReviewToken
        fields = ['type_of_review', 'which_restaurant', 'which_dish']

class AddRatingRestaurantForm(forms.ModelForm):

    class Meta:
        model = RatingRestaurant
        fields = ['description', 'rating_number']

class AddRatingDishForm(forms.ModelForm):

    class Meta:
        model = RatingDish
        fields = ['description', 'rating_number']