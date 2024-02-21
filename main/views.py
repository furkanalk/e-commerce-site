from django.shortcuts import render, get_object_or_404
from pazar.models import Product     
from profiller.models import Userprofile, SaticiBasvuru, PremiumBasvuru
from .models import Carousel

def showAnaSayfa(request):
    products = Product.objects.filter(status=Product.ACTIVE)
        
    for product in products:
        if product.user.userprofiles.premium_mu == True:
            product.premium = True
            product.save()
        else:
            product.premium = False
            product.save()
    
    showproducts = Product.objects.filter(status = Product.ACTIVE, premium = False)[0:16]
    showpproducts = Product.objects.filter(status= Product.ACTIVE, premium = True)[0:16]
    
    try:
        premium_basvurdu = get_object_or_404(PremiumBasvuru,user_id = request.user.id)
    except:
        premium_basvurdu = None
        
    try:
        satici_basvurdu = get_object_or_404(SaticiBasvuru,user_id = request.user.id)
    except:
        satici_basvurdu = None
        
    images = Carousel.objects.all()
        
    return render(request, 'main/anasayfa.html', {
        'products': showproducts,
        'pproducts': showpproducts,
        'satici_basvurdu': satici_basvurdu,
        'premium_basvurdu': premium_basvurdu,
        'images': images,
        })

