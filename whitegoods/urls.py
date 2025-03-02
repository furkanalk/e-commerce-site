from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.base.urls')),  
    path('', include('apps.register.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.store.urls')),
    path('', include('apps.submission.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
