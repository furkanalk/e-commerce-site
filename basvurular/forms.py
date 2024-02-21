from django import forms
from profiller.models import SaticiBasvuru

class saticiBasvuruForm(forms.ModelForm):
    
    class Meta:
        model = SaticiBasvuru
        fields = ('company','tel', 'address', 'description')