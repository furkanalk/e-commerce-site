from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Carousel(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = ResizedImageField(max_length=225, size=[1200, 400],upload_to='whitegoods/carousel', blank=True, null=True)
    
    class Meta:
         verbose_name_plural = "Ads"
         
    def __str__(self):
        return self.title