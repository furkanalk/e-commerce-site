from django import forms
from .models import Userprofile

class photoForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['photo'] 
        
        labels = {
        "photo":  "Profil Resim",
        }
        
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            })    
        }