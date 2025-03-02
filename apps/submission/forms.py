from django import forms
from apps.users.models import SellerSubmission

class SellerSubmissionForm(forms.ModelForm):
    class Meta:
        model = SellerSubmission
        fields = ('company', 'phone', 'address', 'description')