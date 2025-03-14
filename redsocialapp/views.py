from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def ingreso(request):
    if request.method == "GET":
        return render(request,'ingreso.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        usuarioAutenticado = authenticate(username = username, password = password)
        if usuarioAutenticado is None:
            return render(request,'ingreso.html',{
                'errorCredenciales': 'Usuario o contraseña no válidos.'
            })
        else:
            login(request,usuarioAutenticado)
            return redirect('inicio')
    
def registro(request):
    if request.method == "GET":
        return render(request,'registro.html')
    else:
        username = request.POST["username"]
        clave1 = request.POST["password1"]
        clave2 = request.POST["password2"]
        if clave1 == clave2:
            try:
                usuarioRegistrado = User.objects.create_user(username = username, password = clave1)
                usuarioRegistrado.save()
                login(request,usuarioRegistrado)
                return redirect('ingreso')
            except IntegrityError:
                return render(request,'registro.html',{
                    'errorUsuarioExistente':"Usuario ya existente con el username ingresado. Por favor vuelva a ingrese otro nuevamente."
                })
        else:
            return render(request,'registro.html',{
                'errorClavesNoIguales': 'Las claves deben coincidir. Vuelva a intentarlo.'
            })
            
@login_required            
def inicio(request):
    return render(request,'inicio.html')
    
def cerrarSesion(request):
    logout(request)
    return redirect('ingreso')