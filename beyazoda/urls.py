from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import showAnaSayfa

urlpatterns = [
    path('', showAnaSayfa, name='anasayfa'),  
    path('admin/', admin.site.urls),
    path('', include('kayit.urls')),
    path('', include('profiller.urls')),
    path('', include('pazar.urls')),
    path('', include('basvurular.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
