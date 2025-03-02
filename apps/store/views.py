import json
import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings

from .models import Product, Category, Order, OrderItem, Comments, QuestionAnswer, Favorites
from .cart import Cart
from .forms import OrderForm, CommentsForm, QnAForm

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('show_cart')

def show_cart(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(str(product_id))
    return redirect('show_cart')

def update_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1 if action == 'increase' else -1
        cart = Cart(request)
        cart.add(product_id, quantity, update_quantity=True)

    return redirect('show_cart')

def order_confirmed(request):
    return render(request, 'store/order_confirmed.html')

@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        data = json.loads(request.body)
        form = OrderForm(request.POST)

        total_price = 0
        items = []

        for item in cart:
            product = item['product']
            total_price += product.price * int(item['quantity'])

            items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': product.title},
                    'unit_amount': product.price * 100
                },
                'quantity': item['quantity']
            })

        # Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url='http://127.0.0.1:8000/cart/order_confirmed/',
            cancel_url='http://127.0.0.1:8000/cart/'
        )
        payment_intent = session.payment_intent

        # Create Order
        order = Order.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            zipcode=data['zipcode'],
            city=data['city'],
            placed_by=request.user,
            payment_completed=True,
            payment_intent=payment_intent,
            amount_paid=total_price,
            product_id=product.id
        )

        # Create Order Items
        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                price=price,
                quantity=quantity,
                user=request.user,
                reviewed=False
            )

            product.total_sold += quantity
            product.save(update_fields=['total_sold'])

        cart.clear()

        return JsonResponse({'session': session, 'order': payment_intent})

    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
    })

def filter_store_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=2)

    sort_option = request.GET.get('sort')

    if sort_option == 'rating':
        products = products.order_by("-average_rating")
    elif sort_option == 'newest':
        products = products.order_by("-created_at")
    elif sort_option == 'oldest':
        products = products.order_by("created_at")
    elif sort_option == 'price_low':
        products = products.order_by("price")
    elif sort_option == 'price_high':
        products = products.order_by("-price")

    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paginated_products = paginator.get_page(page)

    return render(request, 'store/category.html', {
        'category': category,
        'products': paginated_products
    })

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=2)
    category = Category.objects.get(slug=category_slug)
    related_products = Product.objects.filter(category_id=category.id)
    comments = Comments.objects.filter(product_id=product.id, status=1).order_by('-created_at')
    questions = QuestionAnswer.objects.filter(product_id=product.id, status=1).order_by('-id')

    try:
        unanswered_question = QuestionAnswer.objects.get(product_id=product.id, user_id=request.user.id, answered=0)
    except QuestionAnswer.DoesNotExist:
        unanswered_question = None

    try:
        favorite = Favorites.objects.get(user_id=request.user.id, product_id=product.id)
    except Favorites.DoesNotExist:
        favorite = None

    if comments.exists():
        total_rating = sum(comment.rate for comment in comments)
        average_rating = round(total_rating / comments.count(), 1)
    else:
        average_rating = 0

    product.average_rating = average_rating
    product.comment_count = comments.count()
    product.save(update_fields=['average_rating', 'comment_count'])

    url = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        if 'ask_question' in request.POST:
            form = QnAForm(request.POST)
            if form.is_valid():
                QuestionAnswer.objects.create(
                    user=request.user,
                    product=product,
                    question=form.cleaned_data['question']
                )
                messages.success(request, "Your question has been submitted.")
                return HttpResponseRedirect(url)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'comments': comments,
        'questions': questions,
        'favorite': favorite,
        'unanswered_question': unanswered_question,
        'average_rating': average_rating
    })

def store_search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(
        status=Product.ACTIVE
    ).filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query)
    )

    return render(request, 'store/search.html', {
        'query': query,
        'products': products
    })
