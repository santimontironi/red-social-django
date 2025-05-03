from .models import Novedades

def novedadesNuevas(request):
    
    if request.user.is_authenticated: #el if es necesario para asegurarte de que solo realizas la consulta a la base de datos cuando el usuario ha iniciado sesión
        novedadesSinLeer = Novedades.objects.filter(leida=False, user=request.user).exists()
    else:
        novedadesSinLeer = False 

    return {
        'novedadesSinLeer': novedadesSinLeer
    }