from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
 
    class Meta:
         verbose_name = "Müşteriler"
            
    def _str_(self):
        return self.user
    
class Carousel(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = ResizedImageField(max_length=225, size=[1800, 780],upload_to='beyazoda/carousel', blank=True, null=True)
    
    class Meta:
         verbose_name_plural = "Reklamlar"
         
    def __str__(self):
        return str(self.title)