from django.contrib.auth import views as authw
from django.urls import path
from .import views
 
urlpatterns = [  
    path('kayitol/', views.kayitol, name="kayitol"),
    path('girisyap/', authw.LoginView.as_view(template_name='kayit/girisyap.html'), name='girisyap'),
    path('cikisyap/', authw.LogoutView.as_view(), name='cikisyap'),
] 