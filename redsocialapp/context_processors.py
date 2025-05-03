from .models import Novedades

def novedadesNuevas(request):
    novedadesSinLeer = Novedades.objects.filter(leida=False,user=request.user).exists()
    return{
        'novedadesSinLeer':novedadesSinLeer
    }