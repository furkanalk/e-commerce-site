from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Userprofile, SaticiBasvuru, PremiumBasvuru
from .forms import photoForm
from pazar.forms import ProductForm, SoruCevapForm, SCevapForm, DurumForm, YorumlarForm
from kayit.forms import guncelleForm
from django.utils.text import slugify
from pazar.models import Product, SiparisVer, Siparis, Yorumlar, SoruCevap, Favoriler
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
import cloudinary.uploader
import cloudinary

def satici_profil(request, pk):
    user = User.objects.get(pk = pk)
    products = user.products.filter(status=Product.ACTIVE)
    
    thevalue = request.GET.get('name')
    
    for product in products:
        if user.userprofiles.premium_mu == True:
            product.premium = True
            product.save()
        else:
            product.premium = False
            product.save()
        
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
    
    return render(request, 'profiller/saticiprofil.html',
    {
        'user': user,
        'products': products,
        'urunler': urunler
    })

def detaylar(request,pk):
    products = Product.objects.filter(user_id = pk)
    
    try:
        userprofile = get_object_or_404(Userprofile,user_id = pk)
    except:
        userprofile = None
        
    try:
        satici_basvurdu = get_object_or_404(SaticiBasvuru,user_id = request.user.id)
    except:
        satici_basvurdu = None
        
    try:
        premium_basvurdu = get_object_or_404(PremiumBasvuru,user_id = request.user.id)
    except:
        premium_basvurdu = None
        
    product_amount = 0
    howmanysold = 0
    howmuchearned = 0
    comment_amount = 0  
    question_amount = 0
    average_rating = 0
    temp = 0
    
    name = User.objects.get(id=pk)
    
    for product in products:
        if product.average_rating is not "0": 
            average_rating += float(product.average_rating)
            temp += 1     
        comment_amount += int(product.comment_amount)
        howmanysold += int(product.howmany)
        howmuchearned += float(product.howmuch)
        question_amount += int(product.question_amount)
        product_amount += 1
        
    if average_rating is not 0:
        average_rating = average_rating/temp
        average_rating = round(average_rating,1)
        
    return render(request, 'profiller/detaylar.html',{
        'product_amount': product_amount,
        'howmanysold': howmanysold,
        'howmuchearned': howmuchearned,
        'comment_amount': comment_amount,
        'average_rating': average_rating,
        'question_amount': question_amount,
        'products': products,
        'name': name,
        'userprofile': userprofile,
        'satici_basvurdu': satici_basvurdu,
        'premium_basvurdu': premium_basvurdu
    })

def profil_duzenle(request,pk):
    current_user = User.objects.get(id=pk)
    try:
        userp = get_object_or_404(Userprofile,user_id = request.user.id)
    except:
        userp = None
        
    form = guncelleForm(request.POST or None, instance = current_user)
    
    if userp is not None:
        form_photo = photoForm(request.POST or None, request.FILES or None, instance = userp)
    else:
        form_photo = None
    
    if form_photo is None and form.is_valid():
        form.save()
        messages.success(request, ("Profil bilgileriniz başarıyla güncellendi."))
        return redirect('girisyap')   
    elif form.is_valid() and form_photo.is_valid():
        form.save()
        form_photo.save()
        messages.success(request, ("Profil bilgileriniz başarıyla güncellendi."))
        return redirect('girisyap')
    
    return render(request, 'profiller/profil_duzenle.html',{
        'form': form,
        'form_photo': form_photo
    })
    
@login_required
def satici_pazar(request):
    products = request.user.products.exclude(status=Product.DELETED)
    order_items = SiparisVer.objects.filter(beyazesya__user=request.user, yorum=SiparisVer.FALSE).order_by('-id')
    aktif = Product.STATUS_CHOICES[2][1]
    inaktif = Product.STATUS_CHOICES[0][1]
    thevalue = request.GET.get('name')
 
    if thevalue:
        if len(thevalue) > 0:
            productid = thevalue[:-1]
            process = thevalue[len(thevalue) - 1]

        if process == '1':
            data = Product(id = productid)
            data.status = Product.DRAFT
            data.save(update_fields=['status'])
        if process == '2':
            data = Product(id = productid)
            data.status = Product.ACTIVE
            data.save(update_fields=['status'])
        
    return render(request, 'profiller/pazarim.html',{
        'products': products,
        'order_items': order_items,
        'aktif': aktif,
        'inaktif': inaktif
    })

@login_required
def siparis_detay(request, pk, slug):
    siparis = get_object_or_404(Siparis, pk=pk)
    siparisv = Siparis.objects.filter(pk=pk)
    product = Product.objects.all().get(slug = slug)
    siparisver = SiparisVer.objects.get(beyazesya__id = product.id, siparis_id = siparis.id)
    url = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        value = request.POST.get('durum')
        form = DurumForm(instance=siparisver)
        data = SiparisVer(pk = siparisver.id)
        if 'OK' in request.POST:
                data.durum = Siparis.SIPARIS_TESLIM_EDILDI
                data.yorum = SiparisVer.TRUE
                data.save(update_fields=['durum','yorum'])
                return redirect('pazarim')  
  
        if 'GUNCELLE' in request.POST:
            data.durum = str(value)
            data.yorum = SiparisVer.FALSE
            data.save(update_fields=['durum','yorum'])
            return HttpResponseRedirect(url)
                    
    return render(request, 'profiller/siparis_detay.html',{
        'siparis': siparis,
        'siparis_urun': siparisver,
    })
    
@login_required
def siparis_gecmis(request):
    siparis = SiparisVer.objects.exclude(yorum=SiparisVer.FALSE).order_by("-id")
    
    return render(request, 'profiller/gecmis_siparislerim.html',{
        'siparis': siparis,
    })
    
@login_required
def urun_ekle(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()
            
            messages.success(request, 'Ürün başarıyla eklendi.')
            
            return redirect('pazarim')
    else:
        form = ProductForm()
            
    return render(request, 'profiller/urunDuzenle.html', {
        'title' : 'Ürün Ekle',
        'form' : form
    })

@login_required
def urun_duzenle(request,pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    form = ProductForm(request.POST, request.FILES, instance=product)
    formA = SCevapForm(request.POST, instance=product)
    comments = Yorumlar.objects.filter(product_id=pk,status=Yorumlar.TRUE).order_by('-created_at')
    questions = SoruCevap.objects.filter(product_id=product.id,status=SoruCevap.TRUE).order_by('id')
    value = request.GET.get('name')
    qvalue = request.POST.get('theanswer')
    
    if request.method == 'POST':
        if 'duzenle' in request.POST:
            form = ProductForm(request.POST, request.FILES, instance=product)    
            if form.is_valid():
                form.save()
                
                messages.success(request, 'Ürün detayları başarıyla güncellendi.')
                
                return redirect('pazarim')
        
        if 'iptal' in request.POST: 
            form = ProductForm(instance=product)
            
        else:
            if qvalue:
                for question in questions:
                    if  int(qvalue) == question.id:      
                        data = SoruCevap(pk=question.id)
                        data.answer = request.POST.get('answer')
                        data.answered = SoruCevap.TRUE
                        data.save(update_fields=['answer', 'answered'])
                        
                        data = Product.objects.get(pk=pk)
                        soruadet = data.question_amount
                        soruadet += 1
                        data.question_amount = soruadet
                        data.save(update_fields=['question_amount'])
                
              
    form = ProductForm(instance=product)
    
    if value:
        for comment in comments:
            if int(value) == comment.id:
                comment.reported = Yorumlar.TRUE
                comment.save()
                          
    return render(request, 'profiller/urunDuzenle.html', {
        'product': product,
        'form': form,
        'comments': comments,
        'questions': questions,
        'formA' : formA,
    })
     
@login_required
def urun_sil(request,pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    #product.status = Product.DELETED
    #product.save()
    product.image.delete()
    product.delete()
    
    
    
    messages.success(request, 'Ürün basariyla kaldirildi.')
    return redirect('pazarim')

@login_required
def profil_user(request):
    mail = request.user.email
    uname = request.user.username
    fname = request.user.first_name
    lname = request.user.last_name
    password = request.user.password
    products = Product.objects.filter(user=request.user,status=Product.ACTIVE)
    
    try:
        premium_basvurdu = get_object_or_404(PremiumBasvuru,user_id = request.user.id)
    except:
        premium_basvurdu = None
        
    try:
        satici_basvurdu = get_object_or_404(SaticiBasvuru,user_id = request.user.id)
    except:
        satici_basvurdu = None
        
    try:
        myphoto = Userprofile.objects.get(user = request.user)
    except:
        myphoto = None
        
    myproducts = 0
    theaverage_rating = 0
    ratings = 0
    comments = 0
    temp = 0
    for product in products:
        if product.average_rating is not "0": 
            ratings += float(product.average_rating)
            temp += 1
        myproducts += 1
        comments += int(product.comment_amount)
     
    if ratings != 0:   
        theaverage_rating = ratings / temp
        theaverage_rating = round(theaverage_rating,1)

    return render(request, 'profiller/profil.html', {
        'myproducts' : myproducts,
        'mail' : mail,
        'password': password,
        'uname': uname,
        'fname': fname,
        'lname': lname,
        'theaverage_rating': theaverage_rating,
        'myphoto': myphoto,
        'satici_basvurdu': satici_basvurdu,
        'premium_basvurdu': premium_basvurdu
    })

@login_required
def urunlerimi_goster(request):
    idvalue = request.GET.get('product_id')
    productsowned = Product.objects.filter(user=request.user,status=Product.ACTIVE)
    comments = Yorumlar.objects.filter(product_id = idvalue ,status=Yorumlar.TRUE)
    questions = SoruCevap.objects.filter(product_id = idvalue, status=SoruCevap.TRUE)
    siparisler = SiparisVer.objects.filter(beyazesya_id = idvalue)
    
    
    if comments:
        rates = 0
        comment_amount = 0
      
        for comment in comments:
            rates += comment.rate
            comment_amount+=1
        
        average = rates/comment_amount
        average = round(average,1)
    
    else:
        average = 0
        comment_amount = 0
    
    if questions: 
        question_amount = 0    
        
        for question in questions: 
            question_amount +=1
    else:
        question_amount = 0
    
    
    return render(request, 'profiller/urunlerim.html',{
        'productsowned': productsowned,
        'comments': comments,
        'questions': questions,
        'question_amount': question_amount,
        'average': average,
        'comment_amount': comment_amount,
    })
  
@login_required
def siparislerimi_goster(request):
    productsowned = Product.objects.filter(user=request.user,status=Product.ACTIVE)
    siparislerim = Siparis.objects.filter(veren_kisi_id=request.user.id)
    siparisver = SiparisVer.objects.filter(user_id = request.user.id, yorum="False").order_by("-id")
    siparisverYorum = SiparisVer.objects.filter(user_id = request.user.id, yorum="True").order_by("-id")
    siparisverBitti = SiparisVer.objects.filter(user_id = request.user.id, yorum="Done").order_by("-id")
    
    url = request.META.get('HTTP_REFERER')
    #product_id = request.POST.get('yorum_gonder')
    theValue = request.POST.get('yorum_gonder')
    
    if request.method == 'POST':
        product_id = theValue.partition("#")[0]
        siparisv_id = theValue.partition("#")[2]
        if 'yorum_gonder' in request.POST:
            form = YorumlarForm(request.POST)
            if form.is_valid():
                current_user=request.user

                data = Yorumlar()
                data.user_id = current_user.id
                data.product_id = int(product_id)
                data.subject = form.cleaned_data['subject']
                data.comment = form.cleaned_data['comment']
                data.rate = form.cleaned_data['rate']
                rateValue = form.cleaned_data['rate']
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()
                
                data = SiparisVer(pk=siparisv_id)
                data.yorum = SiparisVer.DONE
                data.save(update_fields=['yorum'])
                
                data = Product.objects.get(pk=product_id)
                yorumadet = data.comment_amount
                yorumadet += 1
                data.comment_amount = yorumadet
                allratings = int(data.ratings_toplam)
                allratings += int(rateValue)
                newaverage = allratings/yorumadet
                newaverage = round(newaverage,1)
                data.average_rating = newaverage
                data.save(update_fields=['comment_amount','average_rating'])
                #messages.success(request, "Yorumunuz gönderildi.")
                
                return HttpResponseRedirect(url)
            
    return render(request, 'profiller/siparislerim.html',{
        'productsowned': productsowned,
        'siparislerim': siparislerim,
        'siparisver': siparisver,
        'siparisverYorum': siparisverYorum,
        'siparisverBitti': siparisverBitti
    })

@login_required            
def favorilerim_duzenle(request):
    products = Product.objects.filter(user_id = request.user.id)
    favs = Favoriler.objects.filter(user_id = request.user.id)
    thevalue = request.GET.get('name')
    url = request.META.get('HTTP_REFERER')
    
    if thevalue:
        productid = thevalue.partition(".")[0]
        process = thevalue.partition(".")[2]
        
        try:
            product = get_object_or_404(Product, id = productid)
        except: 
            product = None
            
        try:
            fav = get_object_or_404(Favoriler, user_id = request.user.id , product_id = productid)
        except:
            fav = None
            
        if process == '0':
            data = Favoriler(pk= fav.id)
            data.delete()
            return HttpResponseRedirect(url) 
        
        if process == '1':
            return redirect('pazar', product.category.slug, product.slug)
            
    return render(request, 'profiller/favorilerim.html',{
        'favs': favs,
    })