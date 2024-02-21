from django.urls import path

from .import views

urlpatterns = [
    path('arama/', views.pazarArama, name='arama'),
    path('sepete-ekle/<int:product_id>/', views.sepeteEkle, name='sepete_ekle'),
    path('adet-belirle/<str:product_id>/', views.miktarBelirle, name='miktar_belirle'),
    path('sepetten-kaldir/<int:product_id>/', views.sepettenSil, name='sepetten_kaldir'),
    path('sepetim/', views.sepetiGoster, name='sepeti_goster'),
    path('sepetim/odeme-yap/', views.odeme_yap, name='odeme_yap'),
    path('sepetim/onaylandi/', views.onaylandi, name='onaylandi'),
    path('<slug:slug>/', views.pazarKategori, name='pazarkategori'),
    path('<slug:category_slug>/<slug:slug>/', views.pazarUrunler, name='pazar'),
]
