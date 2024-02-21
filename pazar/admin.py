from django.contrib import admin
from .models import Category, Product, Yorumlar, Siparis, SiparisVer, SoruCevap

class YorumlarAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'product', 'user', 'status']
    list_filter = ['status', 'reported']
  
class SoruCevapAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'product', 'user']
    list_filter = ['status']

class SiparisVerAdmin(admin.ModelAdmin):
    list_display = ['user', 'beyazesya', 'ucret', 'adet', 'durum']
    list_filter = ['durum']
    
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SiparisVer,SiparisVerAdmin)
admin.site.register(Yorumlar,YorumlarAdmin)
admin.site.register(SoruCevap,SoruCevapAdmin)

