from django.contrib import admin
from .models import UserProfile, SellerSubmission, PremiumSubmission

class SellerSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'phone', 'address', 'description']

admin.site.register(UserProfile)
admin.site.register(SellerSubmission, SellerSubmissionAdmin)
admin.site.register(PremiumSubmission)
