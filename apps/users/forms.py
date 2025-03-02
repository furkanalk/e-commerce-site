from django import forms
from .models import UserProfile

class PhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo'] 
        
        labels = {
        "photo":  "Profile Picture",
        }
        
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            })    
        }