from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddReviewTokenForm, AddRatingRestaurantForm, AddRatingDishForm
from django.contrib import messages
from restaurant_stores.models import Restaurant, Dish
from json import loads
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from accounts.models import CustomUser as User
from .models import ReviewToken, RatingRestaurant, RatingDish
from .middleware import restaurant_required_middleware

@restaurant_required_middleware
def create_token_review(req):
    if req.method == 'POST':

        form = AddReviewTokenForm(req.POST)

        if form.is_valid():
            review_token = form.save(commit=False)
            if not User.objects.filter(username=req.POST['for_user']).exists():
                messages.error(req, 'User you have provided Does Not Exist')
                return redirect('/reviews/create_token_review/')
            review_token.for_user = User.objects.get(username=req.POST['for_user'])
            review_token.save()
            review_token.send_token_via_email()
            messages.success(req, f'Token Added Successfully To "{review_token.for_user}"')
            return redirect('/reviews/create_token_review/')
        else:
            messages.error(req, form.errors)
            return redirect('/reviews/create_token_review/')
        
    restaurants = Restaurant.objects.filter(user=req.user)
    context = {
        "title" : "Create Token",
        "resturants" : restaurants,
    }
    return render(req, "reviews/create_token.html", context=context)

@restaurant_required_middleware
@require_POST
def get_dishes(req):

    if not Restaurant.objects.filter(user=req.user, pk=loads(req.body).get("restaurant_id")).exists():
        return JsonResponse({"dishes" : []}, status=200)
    
    if not loads(req.body).get("restaurant_id"):
        return JsonResponse({"dishes" : []}, status=200)
    
    restaurant_id = loads(req.body).get("restaurant_id")
    dishes = Dish.objects.filter(restaurant=restaurant_id)
    return JsonResponse({"dishes" : [{"pk" : dish.pk, "name" : dish.name} for dish in dishes]}, status=200)

def feedback(req, type, token_id):
    if req.method == 'POST':
        review_token = get_object_or_404(ReviewToken, pk=token_id, is_used=False, for_user=req.user)
        if type == "R":
            form = AddRatingRestaurantForm(req.POST)
            if form.is_valid():
                rating_restaurant = form.save(commit=False)
                rating_restaurant.which = review_token.which_restaurant
                rating_restaurant.user = req.user
                rating_restaurant.save()
                
                review_token.is_used = True
                review_token.save()
                
                messages.success(req, "Your Rating Has Been Added Successfully")
                return redirect(f'/reviews/feedback/{type}/{token_id}')
            else:
                messages.error(req, form.errors)
                return redirect(f'/reviews/feedback/{type}/{token_id}')
            
        elif type == "D":
            form = AddRatingDishForm(req.POST)
            if form.is_valid():
                rating_dish = form.save(commit=False)
                rating_dish.which = review_token.which_dish
                rating_dish.user = req.user
                rating_dish.save()
                
                review_token.is_used = True
                review_token.save()
                
                messages.success(req, "Your Rating Has Been Added Successfully")
                return redirect('/')
            else:
                messages.error(req, form.errors)
                return redirect(f'/reviews/feedback/{type}/{token_id}')
             
    context = {
        "title": "Feedback",
        "review_token": get_object_or_404(ReviewToken, pk=token_id),
    }
    return render(req, "reviews/feedback.html", context)

def pending_review_token(req):
    review_tokens = ReviewToken.objects.filter(for_user=req.user, is_used=False).all()
    context = {
        "title" : "Pending Review Tokens",
        "review_tokens" : review_tokens
    }
    return render(req, "reviews/pending_review_tokens.html", context)

