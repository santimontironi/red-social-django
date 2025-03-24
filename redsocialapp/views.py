from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PerfilForm,PublicacionForm
from .models import Publicacion,Perfil
from django.db.models import Q

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
                return redirect('crear-perfil')
            except IntegrityError:
                return render(request,'registro.html',{
                    'errorUsuarioExistente':"Usuario ya existente con el username ingresado. Por favor vuelva a ingrese otro nuevamente."
                })
        else:
            return render(request,'registro.html',{
                'errorClavesNoIguales': 'Las claves deben coincidir. Vuelva a intentarlo.'
            })
            
@login_required
def crearPerfil(request):
    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES)  # Crear el formulario con los datos ingresados
        perfil = form.save(commit=False)  # No guarda aún, permite modificar antes
        perfil.user = request.user  # Asocia el perfil con el usuario actual
        perfil.save()  # Guarda finalmente
        return redirect('inicio')
    else:
        form = PerfilForm()  # Muestra un formulario vacío para crear el perfil
        return render(request,'crearPerfil.html',{
            'form':form
        })

            
@login_required            
def inicio(request):
    if request.method == "GET":
        amigos = request.user.perfil.amigos.all() 
        publicaciones = Publicacion.objects.filter(autor__in=amigos) | Publicacion.objects.filter(autor=request.user)
        publicaciones = publicaciones.order_by('-fechaPublicacion')
        if publicaciones.exists():
            return render(request,'inicio.html', {
                'publicaciones':publicaciones
            })
        else:
            return render(request,'inicio.html',{
                'noHayPublicaciones': True
            })
            
@login_required
def agregarPublicacion(request):
    if request.method == "GET":
        formPublicacion = PublicacionForm()
        return render(request,'agregarPublicacion.html',{
            'formPublicacion':formPublicacion
        })
    else:
        formPublicacion = PublicacionForm(request.POST,request.FILES)
        nuevaPublicacion = formPublicacion.save(commit=False)
        nuevaPublicacion.user = request.user
        nuevaPublicacion.save()
        return redirect('inicio')
    
        
@login_required
def agregarMeGusta(request, id_post):
    publicacion = get_object_or_404(Publicacion, id=id_post)
    if request.method == "POST":
        if request.user in publicacion.liked_by.all():
            publicacion.liked_by.remove(request.user)
            publicacion.likes -= 1
            liked = False
        else:
            publicacion.liked_by.add(request.user)
            publicacion.likes += 1
            liked = True
            
        publicacion.save()
                    
        respuesta = f"""
                <div class="contenedor-btnLike-{publicacion.id}">
                    <span id="likes-{publicacion.id}">{publicacion.likes} Me gustas</span>
                    <input class="btn-like {'liked' if liked else ''}" type="submit" value="❤️">
                </div>
        """    

        return HttpResponse(respuesta)
    

@login_required
def miPerfil(request):
    perfil = request.user.perfil
    if request.method == "GET":
        cantidadPublicaciones = Publicacion.objects.count()
        formularioPerfil = PerfilForm(instance=perfil)
        misPublicaciones = Publicacion.objects.filter(autor = request.user)
        if misPublicaciones.exists():
            return render(request, 'miPerfil.html', {
                'form': formularioPerfil,
                'cantidadPublicaciones':cantidadPublicaciones,
                'misPublicaciones': misPublicaciones
            })
    else:
        formularioPerfil = PerfilForm(request.POST,request.FILES,instance=perfil)
        perfilEditado = formularioPerfil.save(commit=False)
        perfilEditado.user = request.user
        perfilEditado.save()
        return redirect('inicio')
        
        
@login_required
def buscarUsuarios(request):
    if request.method == "POST":
        busqueda = request.POST["busquedaUsuarios"]
        usuarios = Perfil.objects.filter(
            Q(nombre__icontains=busqueda) | Q(apellido__icontains=busqueda) | Q(user__username__icontains=busqueda)
        )
        if usuarios.exists():
            return render(request,'usuarios.html',{
                'usuarios':usuarios
            })
        else:
            return render(request,'usuarios.html',{
                'usuariosNoEncontrados': 'No hay usuarios con ese nombre. Vuelva a intentarlo.'
            })
   
    return render(request, 'usuarios.html', {'usuarios': []})

@login_required
def agregarAmigos(request):
    if request.method == "POST":
        id_amigo = request.POST.get("id_usuario") #se obtiene el id desde el formulario
        amigo = get_object_or_404(User,id=id_amigo) #Busca al usuario que se quiere agregar como amigo
        perfil = get_object_or_404(Perfil,user = request.user) #busca al usuario que esta dentro de la aplicacion
        
        if amigo in perfil.amigos.all():
            mensaje = "Este usuario ya es tu amigo"
        else:
            perfil.amigos.add(amigo) #agrega de amigo al usuario buscado desde el formulario
            mensaje = "Usuario agregado"
        
        return render(request,'usuarios.html',{
            'amigoAgregado': mensaje
        })
     
@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('ingreso')