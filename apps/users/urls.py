from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [  
    # User Profile
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/<int:pk>/', views.edit_profile, name='edit_profile'),
    path('profile/my-products/', views.my_products, name='my_products'),
    path('profile/my-orders/', views.my_orders, name='my_orders'),
    path('profile/details/<int:pk>/', views.profile_details, name='profile_details'),
    path('profile/favorites/', views.manage_favorites, name='manage_favorites'),

    # Seller Dashboard
    path('my-marketplace/', views.seller_dashboard, name='my_dashboard'),
    path('my-marketplace/order-details/<int:pk>/<slug:slug>/', views.order_details, name='order_details'),
    path('my-marketplace/past-orders/', views.order_history, name='order_history'),
    path('my-marketplace/add-product/', views.add_product, name='add_product'),
    path('my-marketplace/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('my-marketplace/delete-product/<int:pk>/', views.delete_product, name='delete_product'),

    # Seller Public Profile
    path('sellers/<int:pk>/', views.seller_profile, name='seller_profile'),

    # Submission URLs
    path('', include('apps.submission.urls')),
]
