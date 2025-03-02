from django.urls import path
from . import views

app_name = 'submission'

urlpatterns = [  
    path('seller-submission/', views.seller_submission, name="seller_submission"),
    path('premium-submission/', views.premium_submission, name="premium_submission"),
]
