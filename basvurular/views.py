from django.shortcuts import render, redirect,  get_object_or_404
from .forms import saticiBasvuruForm
from django.contrib import messages
from pazar.models import Product
from .models import BasvuruReq
from profiller.models import Userprofile,User,SaticiBasvuru,PremiumBasvuru

def satici_basvuru(request):
    form = saticiBasvuruForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            basvuru = form.save(commit=False)
            basvuru.user_id = request.user.id
            basvuru.save()
            return redirect('anasayfa')
        
    return render(request, 'basvurular/satici_basvuru.html',{
        'form': form
    })
    
def premium_basvuru(request):
    products = Product.objects.filter(user_id = request.user.id)
    requirements = BasvuruReq.objects.get(id=1)
    howmanysold = 0
    comment_amount = 0  
    average_rating = 0
    temp = 0
    
    for product in products:
        if product.average_rating is not "0": 
            average_rating += float(product.average_rating)
            temp += 1
        
        comment_amount += int(product.comment_amount)
        howmanysold += int(product.howmany)
        
    if average_rating is not 0:
        average_rating = average_rating/temp
        average_rating = round(average_rating,1)
    
    basvur = request.GET.get('name')
    
    if basvur:
        data = PremiumBasvuru()
        data.user_id = request.user.id
        data.yorum_sayisi = comment_amount
        data.satis_miktari = howmanysold
        data.ortalama_rating = average_rating
        data.save()
        return redirect('anasayfa')
        
    return render(request, 'basvurular/premium_basvuru.html',{
        'howmanysold': howmanysold,
        'comment_amount': comment_amount,
        'average_rating': average_rating,
        'requirements': requirements
    })