from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from accounts.models import CustomUser, OTP
from restaurant_stores.models import Restaurant
from .form_validator import is_valid_email, is_valid_username,is_valid_password
from random import randint
from json import loads
from .forms import CustomUserUpdateForm, ChangeUsernameForm, ChangePasswordForm, ChangeEmailForm
from utils.cloudinary import upload_to_cloudinary

def loginUser(req):
    if req.method == 'POST':

        form = req.POST
        password = form['password']
        if form['email'] != '':
            user =  CustomUser.objects.get(email=form['email']) if CustomUser.objects.filter(email=form['email']).exists() else None
            
            if user is None or not CustomUser.check_password(user, password):
                messages.error(req, 'Login Failed, Invalid Credentials')
                return redirect('/accounts/login')
            
        else:
            username = form['username']
            user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, 'Login Successful')
            return redirect('/')
        else :
            messages.error(req, 'Login Failed, Invalid Credentials')
            return redirect('/accounts/login')
    else :
        context = {
            'title' : 'Login Here'
        }
        return render(req, 'accounts/login.html', context=context)

def signup(req):
    if req.method == 'POST':
        redirection_url = '/accounts/signup/'
        form = req.POST

        if form['email'] == '' or form['username'] == '' or form['password'] == '' or form['confirm_password'] == '':
            messages.error(req, 'All fields are required')
            return redirect(redirection_url)
        
        if CustomUser.objects.filter(username=form['username']).exists():
            messages.error(req, 'Username already exists')
            return redirect(redirection_url)
        
        if not is_valid_username(form['username']):
            messages.error(req, 'Invalid Username')
            return redirect(redirection_url)

        if CustomUser.objects.filter(email=form['email']).exists():
            messages.error(req, 'Email already exists')
            return redirect(redirection_url)
        
        if not is_valid_email(form['email']):
            messages.error(req, 'Invalid Email')
            return redirect(redirection_url)

        if not is_valid_password(form['password']):
            messages.error(req, 'Invalid Password')
            return redirect(redirection_url)

        if form['password'] != form['confirm_password']:
            messages.error(req, 'Passwords do not match')
            return redirect(redirection_url)

        user = CustomUser.objects.create_user(form['username'], form['email'], form['password'])
        user.save()
        messages.success(req, 'Signup Successful')
        loginUser(req)
        return redirect('/')

    else:
        context = {
            'title' : 'Signup Here'
        }
        return render(req, "accounts/signup.html", context=context)

def logoutUser(req):
    logout(req)
    messages.success(req, 'Logout Successful')
    return redirect('/accounts/login')

def profile(req):
    custom_user = CustomUser.objects.get(username=req.user)
    user_restaurants = Restaurant.objects.filter(user=custom_user).all() if Restaurant.objects.filter(user=custom_user).all().exists() else None
    custom_user = {
        "date_of_birth" : custom_user.date_of_birth,
        "biography" : custom_user.biography,
        "email": custom_user.email,
        "full_name" : custom_user.get_full_name(),
        "gender" : custom_user.gender,
        "is_email_verified" : custom_user.is_email_verified,
        "is_phone_verified" : custom_user.is_phone_verified,
        "username" : custom_user.username,
        "profile_picture_url" : custom_user.profile_picture_url,
        "phone_country_code" : custom_user.phone_country_code,
        "phone" : custom_user.phone
    }
    if user_restaurants is not None:
        for u_r in user_restaurants:
            u_r = {
                "name" : u_r.name,
                "description" : u_r.description,
                "logo_url" : u_r.logo_url,
                "pk" : u_r.pk
            }
    context = {
        'title' : "Your Profile",
        'custom_user' : custom_user,
        'user_restaurants' : user_restaurants
    }
    return render(req, "accounts/profile.html", context=context)

def verify_email(req):
    if req.user.is_email_verified:
        return redirect("/accounts/profile")

    elif req.method == 'POST':

        form = req.POST
        otp = form['otp']

        if OTP.objects.filter(user=req.user, type_Of_otp="email", otp=otp).exists():
            email_otp = OTP.objects.get(user=req.user, type_Of_otp="email", otp=otp)
            email_otp.user.is_email_verified = True
            email_otp.user.save()
            email_otp.delete()
            return redirect('/accounts/profile')
        else:
            messages.error(req, 'Invalid OTP')
            return redirect('/accounts/verify_email')
    else:
        context = {
            "title" : "Verify Your E-mail",
            # "js" : "accounts/js/verify_email.js"
        }

        return render(req, 'accounts/verify_email.html', context)

@require_POST
def generate_email_otp(req):
    email = loads(req.body).get('email')
    otp = randint(100000, 999999)
    user = CustomUser.objects.get(email=email)

    if not user.is_email_verified:

        email_otp = OTP.objects.create(
            user = user,
            type_Of_otp = "email",
            otp = otp
        )
        email_otp.save()
        try:
            email_otp.send_otp_via_email(email, otp)
        except Exception as e:
            JsonResponse({"status" : "error", "message" : "Server Not Responsing" + e}, status=500)
        return JsonResponse({"status" : "success", "message" : "OTP Sent successfully to your email"}, status=200)

    return JsonResponse({"status" : "error", "message" : "Email already verified"}, status=400)

@require_POST
def change_profile_picture(req):
    if req.method != 'POST':
        return JsonResponse({"status" : "error", "message" : "Invalid Request"}, status=400)
    
    if not req.user.is_authenticated:
        return JsonResponse({"status" : "error", "message" : "Unauthorized User"}, status=401)

    if req.FILES.get('profile_picture') is None:
        return JsonResponse({"status" : "error", "message" : "Profile Picture is required"}, status=400)
    
    try:

        file = req.FILES['profile_picture']
        profile_picture_url = upload_to_cloudinary(file)

        if profile_picture_url is None:
            return JsonResponse({"status" : "error", "message" : "Server Not Responsing"}, status=500)
        
        req.user.profile_picture_url = profile_picture_url
        req.user.save()


    except Exception as e:
        return JsonResponse({"status" : "error", "message" : str(e)}, status=500)

    messages.success(req, 'Profile Picture Updated')
    return redirect('/accounts/profile')

def update_user_details(req):
    if req.method == 'POST':
        form = CustomUserUpdateForm(req.POST)
        if form.is_valid():
            user = CustomUser.objects.get(username=req.user)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.user_type = form.cleaned_data['user_type']
            user.gender = form.cleaned_data['gender']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.biography = form.cleaned_data['biography']
            user.save()
            messages.success(req, 'User Details Updated')
            return redirect('/accounts/profile')
        else:
            messages.error(req, form.errors)
            return redirect('/accounts/update_user_details')
        
    customUser = CustomUser.objects.only("user_type", "date_of_birth", "biography", "gender", "first_name", "last_name").get(username=req.user)
    context = {
        "title" : "Update User Details",
        "js" : "accounts/js/update_user_details_flowbite.js",
        "customUser" : customUser
    }
    return render(req, "accounts/update_user_details.html", context=context)

def change_username(req):
    if req.method == 'POST':
        form = ChangeUsernameForm(req.POST)
        if form.is_valid():
            user = CustomUser.objects.get(username=req.user) 
            user.username = form.cleaned_data['username']
            if not user.check_password(form.cleaned_data['password']):
                messages.error(req, 'Invalid Password')
                return redirect('/accounts/change_username')
            user.save()
            messages.success(req, 'Username Updated')
            return redirect('/accounts/profile')
        else:
            messages.error(req, form.errors)
            return redirect('/accounts/change_username')
    
    context = {
        "title" : "Change Username",
    }
    return render(req, "accounts/change_username.html", context=context)

def change_password(req):
    if req.method == 'POST':
        form = ChangePasswordForm(req.POST)
        if form.is_valid():
            user = CustomUser.objects.get(username=req.user)
            if not user.check_password(form.cleaned_data['old_password']):
                messages.error(req, 'Invalid Old Password')
                return redirect('/accounts/change_password')
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(req, 'Password Updated')
            login(req, user)
            return redirect('/accounts/profile')
        else:
            messages.error(req, form.errors)
            return redirect('/accounts/change_username')
    
    context = {
        "title" : "Change Password",
    }

    return render(req, "accounts/change_password.html", context=context)

def change_email(req):
    if req.method == 'POST':
        form = ChangeEmailForm(req.POST)
        if form.is_valid():
            user = CustomUser.objects.get(username=req.user)
            if not user.check_password(form.cleaned_data['password']):
                messages.error(req, 'Invalid Password')
                return redirect('/accounts/change_email')
            user.email = form.cleaned_data['email']
            user.is_email_verified = False
            user.save()
            messages.success(req, 'Email Updated')
            return redirect('/accounts/profile')
        else:
            messages.error(req, form.errors)
            return redirect('/accounts/change_email')
    
    context = {
        "title" : "Change Email",
    }

    return render(req, "accounts/change_email.html", context=context)