import re
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            re.compile(r'^/admin/.*$'),
            re.compile(r'^/accounts/login/$'),
            re.compile(r'^/accounts/signup/$'),
            re.compile(r'^/$'),
            re.compile(r'^/restaurant_stores/$'),
            re.compile(r'^/store/\d+/$'),
        ]

        # Allow static and media files to be accessed without login
        if settings.DEBUG:
            exempt_urls += [
                re.compile(r'^/static/.*$'),
                re.compile(r'^/media/.*$'),
            ]

        # Check if the request path is in the exempt URLs
        path = request.path_info
        if not request.user.is_authenticated:
            if not any(url.match(path) for url in exempt_urls):
                print(f"Login Required for URL = {path}")
                return redirect(settings.LOGIN_URL)
                
        response = self.get_response(request)
        return response
