from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', view=views.loginUser, name='login'),
    path('signup/', view=views.signup, name='signup'),

    path('logout/', view=views.logoutUser, name='logout'),
    path('profile/', view=views.profile, name='profile'),


    path('verify_email/', view=views.verify_email, name='verify_email'),
    path('generate_email_otp/', view=views.generate_email_otp, name='generate_email_otp'),

    path('change_profile_picture/', view=views.change_profile_picture, name='change_profile_picture'),
    path('update_user_details/', view=views.update_user_details, name='update_user_details'),

    path('change_username/', view=views.change_username, name='change_username'),
    path('change_password/', view=views.change_password, name='change_password'),
    path('change_email/', view=views.change_email, name='change_email')
]