from .sepet import Sepet

def sepet(request):
    return {'sepet': Sepet(request)}