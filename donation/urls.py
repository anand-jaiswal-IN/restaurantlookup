from django.urls import path
from . import views

app_name = 'donation'

urlpatterns = [
    path('', view=views.donation_page, name='donation_page'),
    path('create_razorpay_order/' , view=views.create_razorpay_order, name='create_razorpay_order')
]