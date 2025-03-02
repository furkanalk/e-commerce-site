from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profiles', on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    photo = ResizedImageField(
        max_length=225, 
        size=[190, 210], 
        upload_to='whitegoods/profile_pictures', 
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name_plural = "Sellers"
    
    def __str__(self):
        return self.user.username

class SellerSubmission(models.Model):
    user = models.OneToOneField(User, related_name='seller_submission', on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    address = models.TextField(max_length=100)
    description = models.TextField(max_length=100)

    class Meta:
        verbose_name_plural = "Seller Submissions"

    def __str__(self):
        return self.user.username

class PremiumSubmission(models.Model):
    user = models.OneToOneField(User, related_name='premium_submission', on_delete=models.CASCADE)
    comment_count = models.CharField(max_length=100)
    sales_amount = models.CharField(max_length=100)
    average_rating = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Premium Submissions"

    def __str__(self):
        return self.user.username
