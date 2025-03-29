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
        sessionActiva = request.POST.get("sessionActiva", "off") == "on"
        usuarioAutenticado = authenticate(request,username = username, password = password)
        if usuarioAutenticado is None:
            return render(request,'ingreso.html',{
                'errorCredenciales': 'Usuario o contraseña no válidos.'
            })
        else:
            print("PASO 1")
            if sessionActiva:
                request.session.set_expiry(1209600)
                print("PASO 2")
            else:
                print("PASO 3")
                request.session.set_expiry(0)
            request.session.modified = True
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
        cantidadPublicaciones = Publicacion.objects.filter(autor=request.user).count()
        formularioPerfil = PerfilForm(instance=perfil)
        misPublicaciones = Publicacion.objects.filter(autor = request.user)
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
   
    return render(request, 'usuarios.html')

@login_required
def agregarAmigos(request):
    if request.method == "POST":
        id_amigo = request.POST.get("id_usuario") #se obtiene el id desde el formulario
        amigo = get_object_or_404(User,id=id_amigo) #Busca al usuario que se quiere agregar como amigo
        perfil = get_object_or_404(Perfil,user = request.user) #busca al usuario que esta dentro de la aplicacion
        
        if amigo in perfil.amigos.all():
            perfil.amigos.remove(amigo) #se elimina al amigo en caso de ya serlo
            respuesta = f"""
                <button class="btn btn-success" id="boton-{amigo.id}">Agregar a amigos</button>
            """    
        else:
            perfil.amigos.add(amigo) #agrega de amigo al usuario buscado desde el formulario
            respuesta = f"""
                <button class="btn btn-success" id="boton-{amigo.id}">Amigo</button>
            """
        
        return HttpResponse(respuesta)
        
        
def verUsuario(request,id_usuario):
    usuario = get_object_or_404(Perfil,id=id_usuario)
    publicaciones = Publicacion.objects.filter(autor=usuario.user)
    totalPublicaciones = Publicacion.objects.filter(autor=usuario.user).count()
    totalAmigos = usuario.amigos.count()
    if publicaciones:
        return render(request,'usuario.html',{
            'usuario':usuario,
            'publicaciones':publicaciones,
            'totalPublicaciones':totalPublicaciones,
            'totalAmigos':totalAmigos
        })
    else:
        noHayPublicaciones = "Este usuario aún no tiene publicaciones."
        return render(request,'usuario.html',{
            'usuario':usuario,
            'noHayPublicaciones':noHayPublicaciones,
            'totalAmigos':totalAmigos,
            'totalPublicaciones':totalPublicaciones,
        })
     
def misAmigos(request):
    amigos = request.user.perfil.amigos.all()
    if amigos:
        hayAmigos = True
        return render(request,'misAmigos.html',{
            'amigos':amigos,
            'hayAmigos':hayAmigos
        })
    else:
        return render(request,'misAmigos.html',{
            'noHayAmigos':'Todavia no has agregado a ningun amigo.',
        })
     
def eliminarAmigo(request):
    if request.method == "POST":
        id_amigo = request.POST.get("idAmigo") #se obtiene el id desde el formulario    
        perfil = get_object_or_404(Perfil,user=request.user) #se obtiene el perfil del usuario que esta logueado
        amigo = get_object_or_404(User,id=id_amigo) #se obtiene al usuario desde el modelo User
        perfil.amigos.remove(amigo) #se elimina ese amigo del modelo 
        
    return redirect('mis-amigos')
    
     
@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('ingreso')