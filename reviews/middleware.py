from django.utils.deprecation import MiddlewareMixin
from .models import Restaurant
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import decorator_from_middleware

class RestaurantRequiredMiddleware(MiddlewareMixin):
    def process_request(self, req):
        # Code to execute for each request before the view (and later middleware) are called.
        if not Restaurant.objects.filter(user=req.user).exists():
            messages.error(req, "You are not authorized to access this page because you are not a restaurant owner")
            return redirect("/accounts/profile/")

    def process_response(self, request, response):
        # Code to execute for each request/response after the view is called.
        return response
    
restaurant_required_middleware = decorator_from_middleware(RestaurantRequiredMiddleware)