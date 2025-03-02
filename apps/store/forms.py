from django import forms
from .models import Product, Order, Comments, QuestionAnswer, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'zipcode', 'city') 


class ProductForm(forms.ModelForm):     
    class Meta:
        model = Product
        fields = ('category', 'title', 'image', 'description', 'price', 'brand', 'model', 
                  'power_consumption', 'energy_class', 'size', 'color', 'details', 'detail_image')
        
        labels = {
            "category": "Category",
            "title": "Name",
            "description": "Short Description",
            "price": "Price ($)",
            "brand": "Brand",
            "model": "Model",
            "power_consumption": "Power Consumption (W)",
            "energy_class": "Energy Class",
            "size": "Size",
            "color": "Color",
            "details": "Details (Other)",
            "detail_image": "Detail Image",
            "image": "Product Image",
        }
        
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder': 'Enter product name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder': 'Enter product description', 'rows': '2',
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder': 'Enter product price',
            }),
            'brand': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder': 'Enter product brand',
            }),
            'model': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder': 'Enter product model',
            }),
            'power_consumption': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder': 'Enter power consumption',
            }),
            'energy_class': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder': 'Enter energy class',
            }),
            'size': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder': 'Enter product size',
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200', 'placeholder': 'Enter product color',
            }),
            'details': forms.Textarea(attrs={
                'class': 'w-full h-1/2 p-4 border border-gray-200', 'placeholder': 'Enter product details',
            }),
            'detail_image': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200',
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200',
            }),        
        } 


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['subject', 'comment', 'rate']


class QnAForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ['question']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ['answer']


class StatusForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['status']
