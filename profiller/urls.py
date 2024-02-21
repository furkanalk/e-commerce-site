from django.contrib.auth import views as authw
from django.urls import path, include

from . import views

urlpatterns = [  
    path('profil/', views.profil_user, name='profil'),
    path('profil/profil-duzenle/<int:pk>/', views.profil_duzenle, name='profil_duzenle'),
    path('profil/urunlerim/', views.urunlerimi_goster, name='urunlerimigoster'),
    path('profil/siparislerim/', views.siparislerimi_goster, name='siparislerimi_goster'),
    path('profil/detaylar/<int:pk>/', views.detaylar, name='detaylar'),
    path('profil/favorilerim/', views.favorilerim_duzenle, name='favorilerim_duzenle'),
    path('pazarim/', views.satici_pazar, name='pazarim'),
    path('pazarim/urun-detaylari/<int:pk>/<slug:slug>/', views.siparis_detay, name='siparis_detay'),
    path('pazarim/gecmis-siparisler/', views.siparis_gecmis, name='siparis_gecmis'),
    path('pazarim/urun-ekle/', views.urun_ekle, name='urunEkle'),
    path('pazarim/urun-duzenle/<int:pk>/', views.urun_duzenle, name='urunDuzenle'),
    path('pazarim/urun-sil/<int:pk>/', views.urun_sil, name= 'urunSil' ),
    path('saticilar/<int:pk>/', views.satici_profil, name='profiller'),
    path('', include('basvurular.urls'))
]