from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofiles', on_delete=models.CASCADE)
    satici_mi = models.BooleanField(default=False)
    premium_mu = models.BooleanField(default=False)
    photo = ResizedImageField(max_length=225, size=[190, 210],upload_to='beyazoda/profile_pictures', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Satıcılar"
        
    def __str__(self):
        return self.user.username


class SaticiBasvuru(models.Model):
    user = models.OneToOneField(User, related_name='saticibasvuru', on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    tel = models.CharField(max_length=11)
    address = models.TextField(max_length=100)
    description = models.TextField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Satıcı Başvuruları"
        
    def __str__(self):
        return self.user.username

class PremiumBasvuru(models.Model):
    user = models.OneToOneField(User, related_name='premiumbasvuru', on_delete=models.CASCADE)
    yorum_sayisi = models.CharField(max_length=100)
    satis_miktari = models.CharField(max_length=100)
    ortalama_rating = models.CharField(max_length=100)   
     
    class Meta:
        verbose_name_plural = "Premium Başvuruları"
        
    def __str__(self):
        return self.user.username