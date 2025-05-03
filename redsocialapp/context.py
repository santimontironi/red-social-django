from .models import Novedades

def novedadesNuevas(request):
    novedadesNuevas = Novedades.objects.filter(leidas=False,user=request.user).exists()
    return{
        'novedadesNuevas':novedadesNuevas
    }