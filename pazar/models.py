from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'Kategoriler'
        
    def __str__(self):
        return self.title
      
class Product(models.Model): 
    DRAFT = 'hidden'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS_CHOICES = (
        (DRAFT, ' Gizli'),
        (WAITING_APPROVAL, ' Onay Bekliyor'),
        (ACTIVE, ' Pazarda'),
        (DELETED, ' Silindi'),
    )
        
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=225)
    description = models.TextField(max_length=290, blank=True)
    brand = models.TextField(max_length = 50)
    model = models.TextField(max_length = 50)
    power_consumption = models.TextField(max_length=20, blank=True)
    energy_class = models.TextField(max_length=5, blank=True)
    size = models.TextField(max_length=100, blank=True)
    color = models.TextField(max_length=100, blank=True, null=True)
    details = RichTextField(max_length=5000, blank=True, null=True)
    detail_image = models.ImageField(upload_to='beyazoda/other_images', blank=True, null=True)
    price = models.IntegerField()
    image = ResizedImageField(max_length=225, size=[300, 300],upload_to='beyazoda/images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)
    howmany = models.IntegerField(default=0)
    howmuch = models.IntegerField(default=0)
    comment_amount = models.IntegerField(default=0)
    question_amount = models.IntegerField(default=0)
    average_rating = models.FloatField(max_length=100, default = "0")
    ratings_toplam = models.CharField(max_length=100, default = "0")
    premium = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Ürünler'
        
    def __str__(self):
        return self.title
    
    def get_display_price(self):
        return self.price
    
class Siparis(models.Model):
    class Meta:
        verbose_name_plural = 'Siparisler'
        
    SIPARIS_VERILDI = 'sipariş verildi'
    SIPARIS_HAZIRLANIYOR = 'sipariş hazırlanıyor'
    SIPARIS_KARGOLANIYOR = 'sipariş kargolanıyor'
    SIPARIS_YOLDA = 'siparişiniz yolda'
    SIPARIS_TESLIM_EDILDI = 'sipariş teslim edildi'
    
    DURUMLAR = (
        (SIPARIS_VERILDI, 'Sipariş verildi'),
        (SIPARIS_HAZIRLANIYOR, 'Sipariş hazırlanıyor'),
        (SIPARIS_KARGOLANIYOR, 'sipariş kargolanıyor'),
        (SIPARIS_YOLDA, 'Siparişiniz yolda'),
        (SIPARIS_TESLIM_EDILDI, 'Sipariş teslim edildi')
    )
    
    TRUE = 'True'
    FALSE = 'False'
    
    STATUS_CHOICES = (
        (TRUE, 'Evet'),
        (FALSE, 'Hayır'),
    )
    
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    zipcode = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    odenen_miktar = models.IntegerField(blank=True, null=True)
    odemesi_yapildi = models.BooleanField(default = False)
    payment_intent = models.CharField(max_length=225, null=True)
    durum = models.CharField(max_length=50, choices = DURUMLAR, default=SIPARIS_VERILDI)
    yorum = models.CharField(max_length=10,choices=STATUS_CHOICES,default=FALSE)
    veren_kisi = models.ForeignKey(User, related_name='siparisler', on_delete=models.SET_NULL, null=True)
    verdigi_tarih = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, related_name='siparisler', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.product)
    
class Yorumlar(models.Model):
    class Meta:
        verbose_name_plural = 'Yorumlar'
    
    TRUE = 'True'
    FALSE = 'False'
    
    STATUS_CHOICES = (
        (TRUE, 'Evet'),
        (FALSE, 'Hayır'),
    )
    
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='comments',on_delete=models.CASCADE)
    subject = models.CharField(max_length=50,blank=True)
    comment = models.TextField(max_length=200,blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default=TRUE)
    reported = models.CharField(max_length=10,choices=STATUS_CHOICES,default=FALSE)
    ip = models.CharField( max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject
    
class SiparisVer(models.Model):
    class Meta:
        verbose_name_plural = 'Siparişler'
    
    SIPARIS_VERILDI = 'Sipariş Verildi'
    SIPARIS_HAZIRLANIYOR = 'Sipariş Hazırlanıyor'
    SIPARIS_KARGOLANIYOR = 'Sipariş Kargolanıyor'
    SIPARIS_YOLDA = 'Siparişiniz Yolda'
    SIPARIS_TESLIM_EDILDI = 'Sipariş Teslim Edildi'
    
    DURUMLAR = (
        (SIPARIS_VERILDI, 'Sipariş verildi'),
        (SIPARIS_HAZIRLANIYOR, 'Sipariş hazırlanıyor'),
        (SIPARIS_KARGOLANIYOR, 'sipariş kargolanıyor'),
        (SIPARIS_YOLDA, 'Siparişiniz yolda'),
        (SIPARIS_TESLIM_EDILDI, 'Sipariş teslim edildi')
    )
    
    TRUE = 'True'
    FALSE = 'False'
    DONE = 'Done'
    
    STATUS_CHOICES = (
        (TRUE, 'Evet'),
        (FALSE, 'Hayır'),
        (DONE, 'Done')
    )
    
    siparis = models.ForeignKey(Siparis, related_name='items', on_delete=models.CASCADE)
    beyazesya = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    ucret = models.IntegerField()
    durum = models.CharField(max_length=50, choices = DURUMLAR, default=SIPARIS_VERILDI)
    adet = models.IntegerField(default=1)
    user = models.ForeignKey(User, related_name='items', on_delete=models.SET_NULL, null=True)
    yorum = models.CharField(max_length=10,choices=STATUS_CHOICES,default=FALSE)
    
    def __str__(self):
        return str(self.beyazesya)
    
class SoruCevap(models.Model):
    class Meta:
        verbose_name_plural = 'Sorular ve Cevaplar'
        
    TRUE = 'True'
    FALSE = 'False'
    
    STATUS_CHOICES = (
        (TRUE, 'Evet'),
        (FALSE, 'Hayır'),
    )
    
    user = models.ForeignKey(User, related_name='question', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='question',on_delete=models.CASCADE)
    question = models.CharField(max_length=200,blank=True)
    answer = models.TextField(max_length=200,blank=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default=TRUE)
    answered = models.CharField(max_length=10,choices=STATUS_CHOICES,default=FALSE)
    reported = models.CharField(max_length=10,choices=STATUS_CHOICES,default=FALSE)
    
    def __str__(self):
        return self.question
    
class Favoriler(models.Model):
    class Meta:
        verbose_name_plural = 'Favoriler'
        
    TRUE = 'True'
    FALSE = 'False'
    
    STATUS_CHOICES = (
        (TRUE, 'Evet'),
        (FALSE, 'Hayır'),
    )
    
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='favorites',on_delete=models.CASCADE)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default=TRUE)