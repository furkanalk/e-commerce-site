from django.conf import settings

from .models import Product

class Sepet(object):
    def __init__(self, request):
        self.session = request.session
        sepet = self.session.get(settings.SEPET_SESSION_ID)
        
        if not sepet:
            sepet = self.session[settings.SEPET_SESSION_ID] = {}
            
        self.sepet = sepet
        
    def __iter__(self):
        for b in self.sepet.keys():
            self.sepet[str(b)]['beyazesya'] = Product.objects.get(pk=b)
            
        for item in self.sepet.values():
            item['toplam_fiyat'] = int(item['beyazesya'].price * item['adet'])
            
            yield item
            
    def __len__(self):
        return sum(item['adet'] for item in self.sepet.values())
    
    def kaydet(self):
        self.session[settings.SEPET_SESSION_ID] = self.sepet
        self.session.modified = True
        
    def ekle(self, product_id, adet=1, update_adet=False):
        product_id = str(product_id)
        
        if product_id not in self.sepet:
            self.sepet[product_id] = {'adet': int(adet), 'id': product_id}
            
        if update_adet:
            self.sepet[product_id]['adet'] += int(adet)
            
            if self.sepet[product_id]['adet'] == 0:
                self.sil(product_id)
                
        self.kaydet()
    
    def sil(self, product_id):
        if product_id in self.sepet:
            del self.sepet[product_id]
            
            self.kaydet()
    
    def temizle(self):
        del self.session[settings.SEPET_SESSION_ID]
        self.session.modified = True
        
    def toplam_ucret(self):
        for b in self.sepet.keys():
            self.sepet[str(b)]['beyazesya'] = Product.objects.get(pk=b)
            
        return int(sum(item['beyazesya'].price * item['adet'] for item in self.sepet.values()))