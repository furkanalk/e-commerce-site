from django import forms
from .models import Product, Siparis, Yorumlar, SoruCevap, SiparisVer

class SiparisForm(forms.ModelForm):
    class Meta:
        model = Siparis
        fields = ('first_name', 'last_name', 'address', 'zipcode', 'city',) 

class ProductForm(forms.ModelForm):     
    class Meta:
        model = Product
        fields = ('category','title','image','description','price','brand','model','power_consumption','energy_class','size','color','details','detail_image')
        
        labels = {
        "category":  "Kategori",
        "title":  "İsim",
        "description":  "Kısa Açıklama",
        "price":  "Fiyat (₺)",
        "brand":  "Marka",
        "model":  "Model",
        "power_consumption":  "Güç Tüketimi (W)",
        "energy_class":  "Enerji Sınıfı",
        "size":  "Boyut",
        "color":  "Renk",
        "details":  "Detaylar (Diğer)",
        "detail_image":  "Detaylar Resim",
        "image":  "Ürün Resim",
        }
        
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder' : 'Ürün ismi giriniz.',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-4 border border-gray-200' , 'placeholder' : 'Ürün açıklaması giriniz.',  'rows' : '2',
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200' , 'placeholder' : 'Ürün fiyatını giriniz.',
            }),
            'brand': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200' , 'placeholder' : 'Ürün markasını giriniz.',
            }),
            'model': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200' , 'placeholder' : 'Ürün modelini giriniz.',
            }),
            'power_consumption': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200' , 'placeholder' : 'Ürün enerji tüketim miktarını giriniz.',
            }),
            'energy_class': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200' , 'placeholder' : 'Ürün enerji sınıfını giriniz.',
            }),
            'size': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200' , 'placeholder' : 'Ürün ebatlarını giriniz.',
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200' , 'placeholder' : 'Ürün rengini giriniz.',
            }),
            'details': forms.Textarea(attrs={
                'class': 'w-full h-1/2 p-4 border border-gray-200' , 'placeholder' : 'Ürün detaylarını giriniz.',
            }),
            'detail_image': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200',
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200',
            }),        
        } 
        
class YorumlarForm(forms.ModelForm):
    class Meta:
        model = Yorumlar
        fields = ['subject','comment','rate']
        
class SoruCevapForm(forms.ModelForm):
    class Meta:
        model = SoruCevap
        fields = ['question']
        
class SCevapForm(forms.ModelForm):
    class Meta:
        model = SoruCevap
        fields = ['answer']
        
class DurumForm(forms.ModelForm):
    class Meta:
        model = SiparisVer
        fields = ['durum']