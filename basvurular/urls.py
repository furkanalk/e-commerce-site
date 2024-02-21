from django.contrib.auth import views as authw
from django.urls import path
from .import views

urlpatterns = [  
    path('satici-basvuru/', views.satici_basvuru, name="satici_basvuru"),
    path('premium-basvuru/', views.premium_basvuru, name="premium_basvuru")
] 