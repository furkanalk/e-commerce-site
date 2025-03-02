from django.shortcuts import render, redirect, get_object_or_404
from .forms import SellerSubmissionForm
from django.contrib import messages
from apps.store.models import Product
from .models import Submission
from apps.users.models import PremiumSubmission

def seller_submission(request):
    form = SellerSubmissionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.user_id = request.user.id
        application.save()
        messages.success(request, "Your seller submission has been sent.")
        return redirect('base:homepage')

    return render(request, 'submission/seller_submission.html', {
        'form': form
    })

def premium_submission(request):
    products = Product.objects.filter(user_id=request.user.id)
    requirements = {
        "comment_count": 10,
        "sales_count": 20,
        "average_rating": 4.0
    }
    
    total_sold = 0
    total_comments = 0  
    average_rating = 0
    rated_products = 0

    # Product stats
    for product in products:
        if product.average_rating != 0: 
            average_rating += float(product.average_rating)
            rated_products += 1
        
        total_comments += int(product.comment_count)
        total_sold += int(product.total_sold)

    # Average rating
    if rated_products != 0:
        average_rating = round(average_rating / rated_products, 1)
    
    apply = request.GET.get('apply')
    
    if apply:
        premium_app = PremiumSubmission()
        premium_app.user_id = request.user.id
        premium_app.comment_count = total_comments
        premium_app.total_sales = total_sold
        premium_app.average_rating = average_rating
        premium_app.save()
        messages.success(request, "Your premium submission has been sent.")
        return redirect('homepage')

    return render(request, 'submission/premium_submission.html', {
        'total_sold': total_sold,
        'total_comments': total_comments,
        'average_rating': average_rating,
        'requirements': requirements
    })
