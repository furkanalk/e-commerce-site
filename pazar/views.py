import json
import stripe
from django.shortcuts import render, get_object_or_404 , redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Product, Category, Siparis, SiparisVer, Yorumlar, SoruCevap, Favoriler
from django.conf import settings
from .sepet import Sepet
from .forms import SiparisForm,YorumlarForm, SoruCevapForm
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

def sepeteEkle(request, product_id):
    sepet = Sepet(request)
    sepet.ekle(product_id)
    
    return redirect('sepeti_goster')

def sepetiGoster(request):
    sepet = Sepet(request)
    
    return render(request, 'pazar/sepetim.html',{
        'sepet': sepet,
    })

def onaylandi(request):
    return render(request, 'pazar/onaylandi.html')

@login_required
def odeme_yap(request):
    sepet = Sepet(request)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        form = SiparisForm(request.POST)
        
        toplam_ucret = 0
        items = []
        
        for item in sepet:
            beyazesya = item['beyazesya']
            toplam_ucret += beyazesya.price * int(item['adet'])
                        
            items.append({
                'price_data': {
                    'currency': 'try',
                    'product_data': {
                        'name': beyazesya.title,
                    },
                    'unit_amount': beyazesya.price * 100
                },
                'quantity': item['adet']
            })
            
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url='http://127.0.0.1:8000/sepetim/onaylandi/',
            cancel_url='http://127.0.0.1:8000/sepetim/'
        )
        payment_intent = session.payment_intent
        
        siparis = Siparis.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            address = data['address'],
            zipcode = data['zipcode'],
            city = data['city'],
            veren_kisi = request.user,
            odemesi_yapildi = True,
            payment_intent = payment_intent,
            odenen_miktar = toplam_ucret,
            product_id = beyazesya.id
        )

        for item in sepet:
            beyazesya = item['beyazesya']
            adet = int(item['adet'])
            fiyat = beyazesya.price * adet
            
            item = SiparisVer.objects.create(siparis=siparis, beyazesya=beyazesya, ucret=fiyat, adet=adet, user_id=request.user.id, yorum="False")
            
            data = Product.objects.get(pk=beyazesya.id)
            yeniadet = data.howmany
            yeniadet += adet
            data.howmany = yeniadet
            yenifiyat = data.howmuch
            
            if beyazesya.user.userprofiles.premium_mu == True:
                yenifiyat += (beyazesya.price * 0.95) * adet
                data.howmuch = yenifiyat 
            else:
                yenifiyat += (beyazesya.price * 0.9) * adet
                data.howmuch = yenifiyat 
                
            data.save(update_fields=['howmany', 'howmuch'])
            
        sepet.temizle()
        
        return JsonResponse({'session': session, 'order': payment_intent})
    else:
        form = SiparisForm()
        
    return render(request, 'pazar/odeme_yap.html',{
        'sepet': sepet,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
    })

def sepettenSil(request, product_id):
    sepet = Sepet(request)
    sepet.sil(str(product_id))
    
    return redirect('sepeti_goster')

def miktarBelirle(request, product_id):
    action = request.GET.get('action','')
    
    if action:
        adet = 1
        
        if action == 'azalt':
            adet = -1
        
        sepet = Sepet(request)
        sepet.ekle(product_id, adet, True)
        
    return redirect('sepeti_goster')
    
def pazarKategori(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE) 

    thevalue = request.GET.get('name')
    
    if thevalue:
        
        if thevalue == '1':
            products = products.order_by("-average_rating")
        if thevalue == '2':
            products = products.order_by("created_at")
        if thevalue == '3':
            products = products.order_by("-created_at")
        if thevalue == '4':
            products = products.order_by("price")
        if thevalue == '5':
            products = products.order_by("-price")
        if thevalue == '6':
            products = products.order_by("id")
        
    p = Paginator(products,8)
    page = request.GET.get('page')
    urunler = p.get_page(page)
    
    return render(request, 'pazar/kategori.html',{
        'category': category,
        'products': products,
        'urunler': urunler
    })

def pazarUrunler(request, category_slug, slug):
    #sepet = Sepet(request)
    #print(sepet.toplam_ucret())
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    category = Category.objects.get(slug = category_slug)
    products = Product.objects.filter(category_id  = category.id)
    comments = Yorumlar.objects.filter(product_id=product.id,status=Yorumlar.TRUE).order_by('-created_at')
    questions = SoruCevap.objects.filter(product_id=product.id,status=SoruCevap.TRUE).order_by('-id')
    
    try:
        no_answer = SoruCevap.objects.get(product_id=product.id,user_id = request.user.id, answered=SoruCevap.FALSE)
    except:
        no_answer = None
        
    try:
        fav = Favoriler.objects.get(user_id = request.user.id, product_id = product.id)
    except:
        fav = None
    
    thevalue = request.GET.get('name')
    
    if comments:
        rates = 0
        amount = 0
      
        for comment in comments:
            rates += comment.rate
            amount+=1
        
        ortalama = rates/amount
        ortalama = round(ortalama,1)
        
        data = Product(id = product.id)
        data.average_rating = ortalama
        data.comment_amount = amount
        data.save(update_fields=['average_rating','comment_amount'])
    else:
        ortalama = 0
        data = Product(id = product.id)
        data.average_rating = ortalama
        data.comment_amount = 0
        data.save(update_fields=['average_rating','comment_amount'])
        
    url = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        if 'soru_gonder' in request.POST:
            form = SoruCevapForm(request.POST)
            if form.is_valid():
                current_user=request.user

                data = SoruCevap()
                data.user_id = current_user.id
                data.product_id = product.id
                data.question = form.cleaned_data['question']
                data.save()
                messages.success(request, "Sorunuz iletildi.")
                
                return HttpResponseRedirect(url)   

    if thevalue:
        if thevalue == '0':
            data = Favoriler()
            data.status = Favoriler.TRUE
            data.product_id = product.id
            data.user_id = request.user.id
            data.save()
            return HttpResponseRedirect(url)
        
        if fav:
            if thevalue == '1':
                data = Favoriler(pk= fav.id)
                data.delete()
                return HttpResponseRedirect(url) 
                   
    #category_slug = get_object_or_404(Category, slug=slug)
    return render(request, 'pazar/pazar.html', {
        'product': product,
        'ortalama': ortalama,
        'comments': comments,
        'questions': questions,
        'fav': fav,
        'no_answer': no_answer,
        'products': products
    })

def pazarArama(request):
    query = request.GET.get('query')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query))
    
    return render(request, 'pazar/arama.html',{
        'query': query,
        'urunler': products
    })