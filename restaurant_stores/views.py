from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import Restaurant, RestaurantImages, Dish, Address, Subfood_category
from reviews.models import RatingRestaurant, RatingDish
from .forms import AddRestaurantForm, AddAddressForm, UpdateRestaurantForm, RestaurantImageLogoForm , AddDishForm, AddRestaurantImageForm
from django.contrib import messages
from json import loads

def home(req):
    context = {
        "title" : "Home Page"
    }
    return render(req, "restaurant_stores/home.html", context=context)

def restaurant_stores(req):
    
    restaurants = Restaurant.objects.all()
    context = {
        "title" : "Nearby Stores",
        'restaurants' : restaurants
    }
    return render(req, "restaurant_stores/restaurant_stores.html", context=context)

def store(req, restaurant_id):

    restaurant = Restaurant.objects.get(id=restaurant_id)
    caraousel_images = RestaurantImages.objects.filter(restaurant=restaurant)
    restaurant_reviews = RatingRestaurant.objects.filter(which=restaurant)
    dishes = Dish.objects.filter(restaurant=restaurant)
    context = {
        "title" : "Store Page",
        "restaurant" : restaurant,
        "restaurant_images" : caraousel_images,
        "restaurant_reviews" : restaurant_reviews,
        "dishes" : dishes
    }
    return render(req, "restaurant_stores/store.html", context=context)

def your_restaurant(req, restaurant_id):
    if req.method == "POST":
        form = UpdateRestaurantForm(req.POST)
        if form.is_valid():
            if Restaurant.objects.filter(user=req.user, id=restaurant_id).exists():
                restaurant = Restaurant.objects.get(id=restaurant_id, user=req.user)
                restaurant.website = form.cleaned_data.get("website")
                restaurant.description = form.cleaned_data.get("description")
                restaurant.opening_hours_from = form.cleaned_data.get("opening_hours_from")
                restaurant.opening_hours_to = form.cleaned_data.get("opening_hours_to")
                restaurant.is_open_now = form.cleaned_data.get("is_open_now")
                restaurant.reason_for_not_opening = form.cleaned_data.get("reason_for_not_opening")
                restaurant.save()
                messages.success(req, f"Successfully updated your restaurant")
                return redirect(f"/your_restaurant/{restaurant_id}/")
            else :
                messages.error(req, "You are not authorized to update this restaurant")
                return redirect(f"/your_restaurant/{restaurant_id}/")
            
        else:
            messages.error(req, form.errors)
            return redirect(f"/your_restaurant/{restaurant_id}/")

    if Restaurant.objects.filter(user=req.user, pk=restaurant_id).exists() :
        restaurant = Restaurant.objects.filter(user=req.user).get(id=restaurant_id)
    else:
        messages.error(req, "Unauthorized user")
        return redirect(f"/accounts/profile/")
    restaurant_images = RestaurantImages.objects.filter(restaurant=restaurant).all()
    restaurant_dishes = Dish.objects.filter(restaurant=restaurant).all()

    context = {
        "title" : "Your Restaurant",
        "restaurant" : restaurant,
        "restaurant_images" : restaurant_images,
        "restaurant_dishes" : restaurant_dishes,
        "js" : "/restaurant_stores/js/your_restaurant.js"
    }
    return render(req, "restaurant_stores/your_restaurant.html", context)

def add_restaurant(req):
    
    if req.method == 'POST':
        form = AddRestaurantForm(req.POST, req.FILES)
        
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.user = req.user
            restaurant.save()
            
            if not req.user.is_restaurant_user_type():
                req.user.set_restaurant_user_type()

            messages.success(req, f"Successfully added your restaurant with name = {restaurant.name}")
            return redirect("/accounts/profile/")
        else:
            messages.error(req, form.errors)
            return redirect("/add_restaurant/")

    else:
        addressData = Address.objects.filter(user=req.user).only("pk")
        context = {
            "title" : "Add Your Restaurant",
            "address" : addressData
        }

    return render(req, "restaurant_stores/add_restaurant.html", context)

def add_address(req):
    if req.method == 'POST':
        form = AddAddressForm(req.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = req.user
            address.save()
            messages.success(req, f"Successfully added an address with city = {address.city}")
            return redirect("/accounts/profile/")
        
        else:
            messages.error(req, form.errors)
            return redirect("/add_address/")
    else:
        context = {
            "title" : "Add Address",
        }
        return render(req, "restaurant_stores/add_address.html", context) 

@require_POST
def delete_restaurant(req):
    try:
        restaurant_id = loads(req.body).get("pk")
        r = Restaurant.objects.get(pk=restaurant_id)
        if r.user != req.user:
            messages.error(req, "Unauthorized User")
            return redirect("/accounts/profile/")
        r.delete()
        messages.success(req, f'{r.name} Restaurant Deleted')
        return JsonResponse({"status" : "success", "message" : f"{r.name} Restaurant Deleted"}, status=200)
    except Exception as e:
        JsonResponse({"status" : "error", "message" : "Server Not Responsing" + e}, status=500)

@require_POST
def delete_restaurant_dish(req):
    try:
        dish_id = loads(req.body).get("pk")
        restro_id = loads(req.body).get("restaurantId")
        restaurant = None
        
        if Restaurant.objects.filter(user=req.user, pk=restro_id).exists():
            restaurant = Restaurant.objects.filter(user=req.user).get(pk=restro_id)
        else:
            messages.error(req, "Unauthorized User")
            return redirect("/accounts/profile/")    
        
        r = Dish.objects.get(pk=dish_id, restaurant=restaurant)
        
        r.delete()
        messages.success(req, f'{r.name} Dish Deleted')
        return JsonResponse({"status" : "success", "message" : f"{r.name} Dish Deleted"}, status=200)
    except Exception as e:
        JsonResponse({"status" : "error", "message" : "Server Not Responsing" + e}, status=500)

@require_POST
def delete_restaurant_image(req):
    try:
        dish_id = loads(req.body).get("pk")
        restro_id = loads(req.body).get("restaurantId")
        restaurant = None

        if Restaurant.objects.filter(user=req.user, pk=restro_id).exists():
            restaurant = Restaurant.objects.filter(user=req.user).get(pk=restro_id)
        else:
            messages.error(req, "Unauthorized User")
            return redirect("/accounts/profile/")    
        
        r = RestaurantImages.objects.get(pk=dish_id, restaurant=restaurant)
        r.delete()
        messages.success(req, f'{r.name} Restaurant Image Deleted')
        return JsonResponse({"status" : "success", "message" : f"{r.name} Restaurant Image Deleted"}, status=200)
    except Exception as e:
        JsonResponse({"status" : "error", "message" : "Server Not Responsing" + e}, status=500)

@require_POST
def update_restaurant_logo(req, restaurant_id):
    try:
        if 'image_logo' in req.FILES:
            form = RestaurantImageLogoForm(req.POST, req.FILES)
            if form.is_valid():
                restaurant = Restaurant.objects.get(id=restaurant_id)
                if restaurant.user != req.user:
                    messages.error(req, "Unauthorized User")
                    return redirect("/accounts/profile/")
                restaurant.image_logo = form.cleaned_data.get("image_logo")
                restaurant.save()
                messages.success(req, f"Successfully updated your restaurant logo")
                return redirect(f"/your_restaurant/{restaurant_id}/")
            else:
                messages.error(req, form.errors)
        else:
            messages.error(req, "No logo image uploaded")
            return redirect(f"/your_restaurant/{restaurant_id}/")
    except Exception as e:
        messages.error(req, f"Something went wrong: {str(e)}")
        return redirect(f"/your_restaurant/{restaurant_id}/")

def add_restaurant_image(req, restaurant_id):
    
    if req.method == 'POST':
        if Restaurant.objects.filter(user=req.user, pk=restaurant_id).exists():
            restaurant = Restaurant.objects.filter(user=req.user).get(pk=restaurant_id)
        else:
            messages.error(req, "Unauthorized User")
            return render("/accounts/profile/")
        
        form = AddRestaurantImageForm(req.POST, req.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.restaurant = restaurant
            image.save()
            messages.success(req, f"Successfully added image to your restaurant {restaurant.name}")
            return redirect(f"/your_restaurant/{restaurant_id}/")
        else:
            messages.error(req, form.errors)
            return redirect(f"/add_restaurant_image/{restaurant_id}/")
    else:
        restaurant = None
        if Restaurant.objects.filter(user=req.user, pk=restaurant_id).exists():
            restaurant = Restaurant.objects.filter(user=req.user).only("id", "name").get(pk=restaurant_id)
        else:
            messages.error(req, "Unauthorized User")
            return redirect("/accounts/profile/")
        
        context = {
            "title" : "Add Restaurant Image",
            "restaurant" : restaurant
        }
        return render(req, "restaurant_stores/add_restaurant_image.html", context)

def add_restaurant_dish(req, restaurant_id):
    if req.method == 'POST':

        if not Restaurant.objects.filter(user=req.user, pk=restaurant_id).exists():
            messages.error(req, "Unauthorized User")
            return render("/accounts/profile/")
        
        restaurant = Restaurant.objects.filter(user=req.user).get(pk=restaurant_id)
        form = AddDishForm(req.POST, req.FILES)    
        if form.is_valid():
            dish = form.save(commit=False)
            dish.restaurant = restaurant
            dish.save()
            subcategories = form.cleaned_data['sub_category']
            dish.sub_category.set(subcategories)  
            messages.success(req, f"Successfully added your dish")
            return redirect(f"/your_restaurant/{restaurant_id}/")
        else:
            messages.error(req, form.errors)
            return redirect(f"/add_restaurant_dish/{restaurant_id}/")
        
    else :
        if Restaurant.objects.filter(user=req.user, pk=restaurant_id).exists():
            restaurant = Restaurant.objects.filter(user=req.user).get(pk=restaurant_id)
        else:
            messages.error(req, "Unauthorized User")
            return redirect("/accounts/profile/")
        context = {
            "title" : "Add Restaurant Dish",
            "subCategories" : Subfood_category.objects.all(),
            "restaurant" : {"name" : restaurant.name, "pk" : restaurant.pk}
        }
        return render(req, "restaurant_stores/add_restaurant_dish.html", context)
    
def dish(req, dish_id):
    if not Dish.objects.filter(pk=dish_id).exists():
        messages.error(req, 'Invalid Dish, Dish does not exists')
        return redirect('/restaurant_stores/')
    
    dish = Dish.objects.get(pk=dish_id)
    review_dish = RatingDish.objects.filter(which=dish).all()
    
    context = {
        "title" : "Dish Page",
        "dish" : dish,
        "review_dish" : review_dish
    }
    return render(req, 'restaurant_stores/dish.html', context)