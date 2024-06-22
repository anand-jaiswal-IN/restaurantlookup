from . import views 
from django.urls import path

app_name = 'reviews'

urlpatterns = [
    path('create_token_review/', view=views.create_token_review, name='create_token_review'),
    path('get_dishes/', view=views.get_dishes, name='get_dishes'),
    
    path('feedback/<str:type>/<int:token_id>/', view=views.feedback, name='feedback'),
    path('pending_review_token', views.pending_review_token, name="pending_review_token")
]
