from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        
    # Category Details
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
        
    def __str__(self):
        return self.title
      
class Product(models.Model): 
    class Meta:
        verbose_name_plural = 'Products'
        
    # Product status choices
    STATUS_CHOICES = (
        (0, 'Hidden'),
        (1, 'Waiting Approval'),
        (2, 'In Store'),
        (3, 'Deleted'),
    )
    
    # Foreign Keys
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)

    # Product Details
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=225)
    description = models.TextField(max_length=290, blank=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    power_consumption = models.CharField(max_length=20, blank=True)
    energy_class = models.CharField(max_length=5, blank=True)
    size = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    details = RichTextField(max_length=5000, blank=True, null=True)
    detail_image = models.ImageField(upload_to='whitegoods/other_images', blank=True, null=True)
    price = models.IntegerField()

    # Images
    image = ResizedImageField(size=[300, 300], upload_to='whitegoods/images', quality=85, force_format="WEBP", blank=True, null=True)

    # Meta Information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    # Statistics
    stock_quantity = models.IntegerField(default=0)
    total_sold = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    question_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    ratings_sum = models.IntegerField(default=0)

    # Flags
    premium = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title

    def get_display_price(self):
        return f"${self.price:.2f}"
    
class Order(models.Model):
    class Meta:
        verbose_name_plural = 'Orders'

    # Order status choices
    ORDER_STATUSES = (
        (0, 'Order placed'),
        (1, 'Order preparing'),
        (2, 'Order shipping'),
        (3, 'Your order is in transit'),
        (4, 'Order delivered')
    )

    # Customer Information
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    zipcode = models.CharField(max_length=225)
    city = models.CharField(max_length=225)

    # Payment Details
    amount_paid = models.IntegerField(blank=True, null=True)
    payment_completed = models.BooleanField(default=False)
    payment_intent = models.CharField(max_length=225, null=True)

    # Order Status
    status = models.IntegerField(
        choices=ORDER_STATUSES,
        default=ORDER_STATUSES[0][0] # Order placed
    )

    # Feedback Flag
    feedback = models.BooleanField(default=False)

    # Relationships
    placed_by = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.SET_NULL,
        null=True
    )
    product = models.ForeignKey(
        'Product',
        related_name='orders',
        on_delete=models.SET_NULL,
        null=True
    )

    # Timestamp
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.product} by {self.first_name} {self.last_name}"

    def get_status_display(self):
        return dict(self.ORDER_STATUSES).get(self.status, "Unknown Status")
    
class Comments(models.Model):
    class Meta:
        verbose_name_plural = 'Comments'

    # Relationships
    user = models.ForeignKey(
        User, 
        related_name='comments', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'Product', 
        related_name='comments', 
        on_delete=models.CASCADE
    )

    # Comment details
    subject = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=200, blank=True)
    rate = models.IntegerField(blank=True)

    # Status flag
    status = models.BooleanField(
        default=False
    )
    
    # Reported flag
    reported = models.BooleanField(
        default=False
    )

    # Metadata
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    
class OrderItem(models.Model):
    class Meta:
        verbose_name_plural = 'Order Items'

    # Order status choices
    ORDER_STATUSES = (
        (0, 'Order placed'),
        (1, 'Order preparing'),
        (2, 'Order shipping'),
        (3, 'Your order is in transit'),
        (4, 'Order delivered')
    )

    # Review status choices
    STATUS_CHOICES = (
        (0, 'No'),
        (1, 'Yes'),
        (2, 'Done')
    )

    # Relationships
    order = models.ForeignKey(
        'Order', 
        related_name='items', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'Product', 
        related_name='items', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, 
        related_name='order_items', 
        on_delete=models.SET_NULL,
        null=True
    )

    # Order item details
    price = models.IntegerField()
    status = models.IntegerField(
        choices=ORDER_STATUSES, 
        default=0
    )
    quantity = models.IntegerField(default=1)

    # Review status
    reviewed = models.IntegerField(
        choices=STATUS_CHOICES, 
        default=0
    )

    def __str__(self):
        return str(self.product)
    
    def get_status_display(self):
        return dict(self.ORDER_STATUSES).get(self.status, "Unknown Status")
    
class QuestionAnswer(models.Model):
    class Meta:
        verbose_name_plural = 'Questions and Answers'

    # Relationships
    user = models.ForeignKey(
        User, 
        related_name='questions', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'Product', 
        related_name='questions', 
        on_delete=models.CASCADE
    )

    # Fields
    question = models.CharField(max_length=200, blank=True)
    answer = models.TextField(max_length=200, blank=True)

    # Status flags
    status = models.BooleanField(
        default=False
    )
    answered = models.BooleanField(
        default=False
    )
    reported = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.question
    
class Favorites(models.Model):
    class Meta:
        verbose_name_plural = 'Favorites'

    # Relationships
    user = models.ForeignKey(
        User, 
        related_name='favorites', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'Product', 
        related_name='favorites', 
        on_delete=models.CASCADE
    )

    # Status field
    status = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.username}'s Favorite - {self.product}"