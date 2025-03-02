from django.shortcuts import render, get_object_or_404
from apps.store.models import Product
from apps.users.models import SellerSubmission, PremiumSubmission
from .models import Carousel

def index(request):
    products = Product.objects.filter(status=Product.STATUS_CHOICES[2][0])  # In Store

    for product in products:
        if product.user.user_profiles.is_premium:
            product.premium = True
        else:
            product.premium = False
        product.save()

    show_products = Product.objects.filter(status=Product.STATUS_CHOICES[2][0], premium=False)[:16]
    show_premium_products = Product.objects.filter(status=Product.STATUS_CHOICES[2][0], premium=True)[:16]

    try:
        premium_applied = get_object_or_404(PremiumSubmission, user_id=request.user.id)
    except:
        premium_applied = None

    try:
        seller_applied = get_object_or_404(SellerSubmission, user_id=request.user.id)
    except:
        seller_applied = None

    images = Carousel.objects.all()

    return render(request, 'base/index.html', {
        'products': show_products,
        'premium_products': show_premium_products,
        'seller_applied': seller_applied,
        'premium_applied': premium_applied,
        'images': images,
    })
