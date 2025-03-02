from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .models import UserProfile, SellerSubmission, PremiumSubmission
from .forms import PhotoForm
from apps.store.forms import ProductForm, AnswerForm, CommentsForm
from apps.register.forms import UpdateForm
from apps.store.models import Product, OrderItem, Order, Comments, QuestionAnswer, Favorites

def seller_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    products = user.products.filter(status=Product.STATUS_CHOICES[2][0])

    sort_option = request.GET.get('name')
    sort_mapping = {
        '1': '-average_rating',
        '2': 'created_at',
        '3': '-created_at',
        '4': 'price',
        '5': '-price',
        '6': 'id',
    }

    if sort_option in sort_mapping:
        products = products.order_by(sort_mapping[sort_option])

    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paginated_products = paginator.get_page(page)

    return render(request, 'users/seller_profile.html', {
        'user': user,
        'products': products,
        'paginated_products': paginated_products
    })

def profile_details(request, pk):
    products = Product.objects.filter(user_id=pk)
    user_profile = UserProfile.objects.filter(user_id=pk).first()
    seller_applied = SellerSubmission.objects.filter(user_id=request.user.id).first()
    premium_applied = PremiumSubmission.objects.filter(user_id=request.user.id).first()

    product_count = products.count()
    total_sold = sum(int(product.stock_quantity) for product in products)
    total_earned = sum(float(product.total_sold) for product in products)
    comment_count = sum(int(product.comment_count) for product in products)
    question_count = sum(int(product.question_count) for product in products)

    valid_ratings = [float(p.average_rating) for p in products if p.average_rating != "0"]
    average_rating = round(sum(valid_ratings) / len(valid_ratings), 1) if valid_ratings else 0

    user_info = get_object_or_404(User, id=pk)

    return render(request, 'users/details.html', {
        'product_count': product_count,
        'total_sold': total_sold,
        'total_earned': total_earned,
        'comment_count': comment_count,
        'question_count': question_count,
        'average_rating': average_rating,
        'products': products,
        'user_info': user_info,
        'user_profile': user_profile,
        'seller_applied': seller_applied,
        'premium_applied': premium_applied
    })

def edit_profile(request, pk):
    current_user = get_object_or_404(User, id=pk)
    user_profile = UserProfile.objects.filter(user_id=request.user.id).first()

    form = UpdateForm(request.POST or None, instance=current_user)
    form_photo = PhotoForm(request.POST or None, request.FILES or None, instance=user_profile) if user_profile else None

    if form.is_valid() and (form_photo is None or form_photo.is_valid()):
        form.save()
        if form_photo:
            form_photo.save()
        messages.success(request, "Your profile has been successfully updated.")
        return redirect('login')

    return render(request, 'users/edit_profile.html', {
        'form': form,
        'form_photo': form_photo
    })
    
@login_required
def seller_dashboard(request):
    products = request.user.products.exclude(status=Product.STATUS_CHOICES[3][0])
    order_items = OrderItem.objects.filter(
        product__user=request.user, 
        reviewed=OrderItem.STATUS_CHOICES[0][0]
    ).order_by('-id')
    
    active_status = Product.STATUS_CHOICES[2][1]
    inactive_status = Product.STATUS_CHOICES[0][1]
    action = request.GET.get('name')

    if action:
        product_id = action[:-1]
        process = action[-1]
        product = get_object_or_404(Product, id=product_id)

        if process == '1':
            product.status = 0
        elif process == '2':
            product.status = 2
        product.save(update_fields=['status'])
        return redirect('users:my_dashboard')

    return render(request, 'users/dashboard.html', {
        'products': products,
        'order_items': order_items,
        'active_status': str(active_status),
        'inactive_status': str(inactive_status)
    })

@login_required
def order_details(request, pk, slug):
    order = get_object_or_404(Order, pk=pk)
    product = get_object_or_404(Product, slug=slug)
    order_item = get_object_or_404(OrderItem, product__id=product.id, order_id=order.id)
    referrer_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        status_value = request.POST.get('status')
        if 'OK' in request.POST:
            order_item.status = Order.ORDER_STATUSES[4][0] # Order delivered
            order_item.reviewed = OrderItem.STATUS_CHOICES[1][0]
            order_item.save(update_fields=['status', 'reviewed'])
            return redirect('users:my_dashboard')

        if 'UPDATE' in request.POST:
            order_item.status = int(status_value)
            order_item.reviewed = OrderItem.STATUS_CHOICES[0][0]
            order_item.save(update_fields=['status', 'reviewed'])
            return HttpResponseRedirect(referrer_url)

    return render(request, 'users/order_details.html', {
        'order': order,
        'order_item': order_item
    })
    
@login_required
def order_history(request):
    orders = OrderItem.objects.exclude(reviewed=OrderItem.STATUS_CHOICES[1][0])
    return render(request, 'users/order_history.html', {'orders': orders})
    
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'Product added successfully.')
            return redirect('users:my_dashboard')
    else:
        form = ProductForm()

    return render(request, 'users/edit_product.html', {
        'form': form
    })

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, user=request.user, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    answer_form = AnswerForm(request.POST or None, instance=product)
    comments = Comments.objects.filter(product_id=pk, status=True).order_by('-created_at')
    questions = QuestionAnswer.objects.filter(product_id=product.id, status=True).order_by('id')

    value = request.GET.get('name')
    qvalue = request.POST.get('theanswer')

    if request.method == 'POST':
        if 'duzenle' in request.POST and form.is_valid():
            form.save()
            messages.success(request, 'Product details updated successfully.')
            return redirect('users:my_dashboard')

        elif 'iptal' in request.POST:
            form = ProductForm(instance=product)

        elif qvalue:
            question_id = int(qvalue)
            question = get_object_or_404(QuestionAnswer, id=question_id)
            question.answer = request.POST.get('answer')
            question.answered = True
            question.save(update_fields=['answer', 'answered'])

            product.question_count += 1
            product.save(update_fields=['question_amount'])

    if value:
        for comment in comments:
            if int(value) == comment.id:
                comment.reported = True
                comment.save()

    return render(request, 'users/edit_product.html', {
        'product': product,
        'form': form,
        'comments': comments,
        'questions': questions,
        'answer_form': answer_form,
    })
     
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, user=request.user, pk=pk)
    product.image.delete()
    product.delete()

    messages.success(request, 'Product deleted successfully.')
    return redirect('users:my_dashboard')

@login_required
def user_profile(request):
    user = request.user
    products = Product.objects.filter(user=user, status=Product.STATUS_CHOICES[2][0])

    premium_applied = PremiumSubmission.objects.filter(user_id=user.id).first()
    seller_applied = SellerSubmission.objects.filter(user_id=user.id).first()
    user_photo = UserProfile.objects.filter(user=user).first()

    product_count = products.count()
    total_comments = sum(int(product.comment_count) for product in products)
    valid_ratings = [float(p.average_rating) for p in products if p.average_rating != "0"]
    average_rating = round(sum(valid_ratings) / len(valid_ratings), 1) if valid_ratings else 0
        
    return render(request, 'users/profile.html', {
        'user': user,
        'product_count': product_count,
        'total_comments': total_comments,
        'average_rating': average_rating,
        'user_photo': user_photo,
        'seller_applied': seller_applied,
        'premium_applied': premium_applied
    })

@login_required
def my_products(request):
    product_id = request.GET.get('product_id')
    products_owned = Product.objects.filter(user=request.user, status=Product.STATUS_CHOICES[2][0])
    comments = Comments.objects.filter(product_id=product_id, status=True)
    questions = QuestionAnswer.objects.filter(product_id=product_id, status=True)
    
    return render(request, 'users/my_products.html', {
        'products_owned': products_owned,
        'comments': comments,
        'questions': questions,
        'question_count': questions.count(),
        'comment_count': comments.count(),
    })
  
@login_required
def my_orders(request):
    products_owned = Product.objects.filter(user=request.user, status=Product.STATUS_CHOICES[2][0])
    my_orders = Order.objects.filter(placed_by_id=request.user.id)
    pending_reviews = OrderItem.objects.filter(user_id=request.user.id, reviewed=0).order_by("-id")
    reviewed_orders = OrderItem.objects.filter(user_id=request.user.id, reviewed=1).order_by("-id")
    completed_orders = OrderItem.objects.filter(user_id=request.user.id, reviewed=2).order_by("-id")

    referrer_url = request.META.get('HTTP_REFERER')
    the_value = request.POST.get('sent_comment')

    if request.method == 'POST' and the_value:
        product_id, orderv_id = the_value.split("#")
        form = CommentsForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = int(product_id)
            review.ip = request.META.get('REMOTE_ADDR')
            review.save()

            order_item = OrderItem.objects.get(pk=orderv_id)
            order_item.reviewed = OrderItem.STATUS_CHOICES[2][0]
            order_item.save(update_fields=['reviewed'])

            product = Product.objects.get(pk=product_id)
            product.comment_count += 1
            total_ratings = int(product.ratings_sum) + review.rate
            new_average = round(total_ratings / product.comment_count, 1)
            product.average_rating = new_average
            product.save(update_fields=['comment_count', 'average_rating'])

            messages.success(request, "Your review has been submitted.")
            return HttpResponseRedirect(referrer_url)

    return render(request, 'users/my_orders.html', {
        'products_owned': products_owned,
        'my_orders': my_orders,
        'pending_reviews': pending_reviews,
        'reviewed_orders': reviewed_orders,
        'completed_orders': completed_orders
    })

@login_required
def manage_favorites(request):
    favorites = Favorites.objects.filter(user_id=request.user.id)
    action = request.GET.get('name')
    referrer_url = request.META.get('HTTP_REFERER')

    if action:
        product_id, process = action.split(".")
        product = get_object_or_404(Product, id=product_id)
        favorite = Favorites.objects.filter(user_id=request.user.id, product_id=product_id).first()

        if process == '0' and favorite:
            favorite.delete()
            messages.success(request, "Product removed from favorites.")
            return HttpResponseRedirect(referrer_url)

        if process == '1':
            return redirect('store:product_detail', product.category.slug, product.slug)

    return render(request, 'users/favorites.html', {
        'favorites': favorites,
    })