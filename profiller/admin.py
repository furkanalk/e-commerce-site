from django.contrib import admin

from .models import Userprofile,SaticiBasvuru, PremiumBasvuru

class SaticiBasvurularAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'tel', 'address', 'description']
    
admin.site.register(Userprofile)
admin.site.register(SaticiBasvuru)
admin.site.register(PremiumBasvuru)
