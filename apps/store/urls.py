from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('search/', views.store_search, name='search'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-quantity/<str:product_id>/', views.update_quantity, name='update_quantity'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/success/', views.order_confirmed, name='success'),
    path('<slug:slug>/', views.filter_store_category, name='filter_category'),
    path('<slug:category_slug>/<slug:slug>/', views.product_detail, name='product_detail'),
]
