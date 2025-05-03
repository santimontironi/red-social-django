from .models import Novedades

def novedadesNuevas(request):
    
    if request.user.is_authenticated:
        novedadesSinLeer = Novedades.objects.filter(leida=False, user=request.user).exists()
    else:
        novedadesSinLeer = False 

    return {
        'novedadesSinLeer': novedadesSinLeer
    }