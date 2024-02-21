from django.db import models

class BasvuruReq(models.Model):
    class Meta:
        verbose_name_plural = 'Gereksinimler'
    
    yorum = models.IntegerField()
    satis = models.IntegerField()
    ortalama = models.FloatField()
    
    def __str__(self):
        return "Gereksinimler Listesi"