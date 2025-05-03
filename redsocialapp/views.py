from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PerfilFormCompleto,PerfilFormReducido,PublicacionForm,ComentarioForm
from .models import Publicacion,Perfil,Novedades
from django.db.models import Q
from django.core.mail import send_mail
import random, secrets
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse

# Create your views here.
def ingreso(request):
    if request.user.is_authenticated: #si la cookie del usuario está, se abre la app en inicio.
        return redirect('inicio')
    
    if request.method == "GET":
        return render(request,'ingreso.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"]

        busquedaUsuario = User.objects.filter(Q(username=username) | Q(perfil__email = username)).first()
        
        if busquedaUsuario:
            usuarioAutenticado = authenticate(request,username = busquedaUsuario.username, password = password)
            if usuarioAutenticado is None:
                return render(request,'ingreso.html',{
                    'errorCredenciales': 'Usuario o contraseña no válidos.'
                })
            else:
                
                if request.POST.get("sessionActiva"):
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                    
                # Si el usuario no tiene el perfil creado, redirigir a crear perfil
                perfil = busquedaUsuario.perfil
                if perfil:
                    if perfil.confirmado == False:
                        login(request,usuarioAutenticado)
                        return redirect('confirmar-usuario',user_id = perfil.user.id)
                    elif perfil.creado == False:
                        login(request,usuarioAutenticado)
                        return redirect('crear-perfil')
                    else:
                        login(request,usuarioAutenticado)
                        return redirect('inicio')
            
            
        
def registro(request):
    if request.method == "GET":
        return render(request, 'registro.html')
    else:
        username = request.POST["username"]
        clave1 = request.POST["password1"]
        clave2 = request.POST["password2"]
        email = request.POST["email"]

        if clave1 != clave2:
            return render(request, 'registro.html', {
                'errorClavesNoIguales': 'Las claves deben coincidir. Vuelva a intentarlo.'
            })
        try:
            usuario = User.objects.create_user(username=username, email=email, password=clave1)
            perfil = Perfil(user=usuario, email=email, confirmado=False)
            perfil.codigo_verificacion = random.randint(100000, 999999)
            perfil.save()

            send_mail(
                subject="Código de verificación",
                message=f"Hola {username}, tu codigo es: {perfil.codigo_verificacion}",
                from_email="santiimontironi@gmail.com",
                recipient_list=[email],
                fail_silently=False
            )

            return redirect('confirmar-usuario',user_id=usuario.id)
            
        except IntegrityError:
            return render(request, 'registro.html', {
                'errorUsuarioExistente': "El nombre de usuario ya existe. Por favor elige otro."
             })
            
            
def confirmarUsuario(request,user_id):
    if request.method == "GET":
        return render(request,'verificarUsuario.html')
    else:
        codigo = request.POST["codigo"]
        try:
            perfil = Perfil.objects.get(user__id = user_id)
            if int(perfil.codigo_verificacion) == int(codigo):
                perfil.confirmado = True
                perfil.save()
                login(request,perfil.user)
                return redirect('crear-perfil')
            else:
                return render(request,'verificarUsuario.html',{
                    'errorCodigoIncorrecto':"El código ingresado es incorrecto. Por favor vuelva a intentarlo."
                })
        except (User.DoesNotExist,Perfil.DoesNotExist):
            return render(request,'verificarUsuario.html',{
                'errorUsuarioNoExistente':"El usuario no existe. Por favor vuelva a intentarlo."
            })
            
            
def enviarToken(request):
    if request.method == "POST":
        emailUsuario = request.POST["email"]
        usuario = User.objects.filter(Q(username=emailUsuario) | Q(perfil__email=emailUsuario)).first()
        if usuario:
            
            token = secrets.token_urlsafe() #se genera un token aleatorio
            
            usuario.perfil.token = token #se le asigna al usuario su token
            usuario.perfil.token_created = timezone.now() #se le asigna al usuario la fecha y hora del token creado
            usuario.perfil.save()
            
            #se genera la url para cambiar clave agregando el id del usuario y el token seguro
            url_cambio_clave = request.build_absolute_uri(reverse('cambiar-clave', args=[usuario.id]) + f"?token={token}")
            
            send_mail(
                subject="Cambio de contraseña.",
                message=f"Hola {usuario.username}, has restablecido tu contraseña de SocialByte. Para cambiarla haz click en este enlace: \n{url_cambio_clave}",
                from_email="santiimontironi@gmail.com",
                recipient_list=[usuario.perfil.email],
                fail_silently=False
            )
            return render(request,'ingreso.html',{
                'mensajeExito':"Se ha enviado un correo electrónico a tu bandeja de entrada."
            })
        else:
            return render(request,'ingreso.html',{
                'errorEmailNoExistente':"El email o nombre de usuario ingresado no existe. Por favor vuelva a intentarlo."
            })
            
    return render(request, "cambiarClave.html", {
        'usuario': usuario
    }) 


def cambiarClave(request,id):
    try:
        usuario = User.objects.get(id = id)
        tiempoLimite = usuario.perfil.token_created + timedelta(hours=1) #se le suma una hora a la hora que fue creado el token
        ahora =  timezone.now() #horario actual
        if ahora > tiempoLimite:
            return render(request,'cambiarClave.html',{
                'tokenExpirado': 'El token de confirmación ha vencido, por favor vuelve a solicitarlo.',
                'usuario': usuario
            })
        if request.method == "POST":
            inputCambiarClave = request.POST["claveNueva"]
            usuario.set_password(inputCambiarClave)
            usuario.perfil.token = None
            usuario.perfil.token_created = None
            usuario.save()
            return render(request,'cambiarClave.html',{
                'cambioCorrecto': 'Contraseña cambiada correctamente, ya puedes iniciar sesión nuevamente en: ',
                'usuario':usuario
            })
        else:
            return render(request,'cambiarClave.html',{
                'usuario':usuario
            })
    except User.DoesNotExist:
        return render(request,'cambiarClave.html',{
            'usuarioNoExistente': 'Error. El usuario correspondiente no es válido.'
        })
            
            
            
@login_required
def crearPerfil(request):
    perfil = Perfil.objects.filter(user = request.user).first()  # se obtiene el primer perfil encontrado con el id del usuario
    if request.method == "POST":
        form = PerfilFormCompleto(request.POST, request.FILES, instance=perfil)  #instance=perfil se usa para editar el perfil existente
        form.save()  # se guarda el perfil
        perfil.creado = True
        perfil.save()
        return redirect('inicio')
    else:
        form = PerfilFormCompleto(instance=perfil)  #instance=perfil se usa para mostrar el formulario con los datos del perfil
    
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
        nuevaPublicacion.autor = request.user
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
            if publicacion.autor != request.user:
                novedad = Novedades(user = publicacion.autor,novedad = f"El usuario {request.user} le ha dado me gusta a tu publicación",post = publicacion)
                novedad.save()
        else:
            publicacion.liked_by.add(request.user)
            publicacion.likes += 1
            liked = True
            
        publicacion.save()
                    
        respuesta = f"""
                <div class="contenedor-btnLike-{publicacion.id} d-flex align-items-center justify-content-center gap-2">
                    <span id="likes-{publicacion.id}">{publicacion.likes}</span>
                    <button class="btn-like {'liked' if liked else ''}" type="submit">❤️</button>
                </div>
        """    

    return HttpResponse(respuesta)
    
    
    
@login_required
def agregarComentario(request):
    idPublicacion = request.POST.get("publicacion_id")
    publicacion = Publicacion.objects.get(id = idPublicacion)
    if request.method == "POST":
        formularioComentario = ComentarioForm(request.POST)
        comentarioRealizado = formularioComentario.save(commit=False)
        comentarioRealizado.autor = request.user
        comentarioRealizado.publicacion = publicacion
        publicacion.cantidadComentarios += 1
        publicacion.save()
        comentarioRealizado.save()
        if publicacion.autor != request.user:
            novedades = Novedades(user = publicacion.autor,novedad = f"El usuario {request.user} ha comentado tu foto.", usuario=request.user, comentario = comentarioRealizado, post=publicacion)
            novedades.save()
        
        return redirect('inicio')
    else:
        formularioComentario = ComentarioForm()
        return render(request,'inicio.html',{
            'formComentario':formularioComentario
        })



@login_required
def miPerfil(request):
    perfil = request.user.perfil
    if request.method == "GET":
        cantidadPublicaciones = Publicacion.objects.filter(autor=request.user).count()
        formularioPerfil = PerfilFormReducido(instance=perfil)
        misPublicaciones = Publicacion.objects.filter(autor = request.user)
        return render(request, 'miPerfil.html', {
            'form': formularioPerfil,
            'cantidadPublicaciones':cantidadPublicaciones,
            'misPublicaciones': misPublicaciones
        })
    else:
        formularioPerfil = PerfilFormReducido(request.POST,request.FILES,instance=perfil)
        perfilEditado = formularioPerfil.save(commit=False)
        perfilEditado.user = request.user
        perfilEditado.save()
        return redirect('mi-perfil')
        
        
        
@login_required
def buscarUsuarios(request):
    if request.method == "POST":
        busqueda = request.POST["buscador"]
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
     
     

@login_required
def misAmigos(request):
    amigos = request.user.perfil.amigos.all()
    cantidadAmigos = request.user.perfil.amigos.all().count()
    if amigos:
        hayAmigos = True
        return render(request,'misAmigos.html',{
            'amigos':amigos,
            'hayAmigos':hayAmigos,
            'cantidadAmigos':cantidadAmigos
        })
    else:
        return render(request,'misAmigos.html',{
            'noHayAmigos':'Todavia no has agregado a ningun amigo.',
        })
        
        
    
@login_required
def agregarAmigos(request):
    if request.method == "POST":
        id_amigo = request.POST.get("id_usuario") #se obtiene el id desde el formulario
        amigo = get_object_or_404(User,id=id_amigo) #Busca al usuario que se quiere agregar como amigo
        perfil = get_object_or_404(Perfil,user = request.user) #busca al usuario que esta dentro de la aplicacion
        
        if amigo in perfil.amigos.all():
            perfil.amigos.remove(amigo)
            perfil.save()
            amigo.perfil.amigos.remove(request.user)
            amigo.perfil.save()
            respuesta = f"""
                <button class="btn btn-success" id="boton-{amigo.id}">Agregar a amigos</button>
            """    
        else:
            perfil.amigos.add(amigo) #agrega de amigo al usuario buscado desde el formulario
            perfil.save()
            amigo.perfil.amigos.add(request.user) #te agregas como amigo del usuario
            amigo.perfil.save()
            novedades = Novedades(user = amigo,novedad = f"El usuario {request.user} te agregó de amigos.",usuario=request.user)
            novedades.save()
            respuesta = f"""
                <button class="btn btn-success" id="boton-{amigo.id}">Amigo</button>
            """
        
        return HttpResponse(respuesta)
     
     
     
@login_required     
def eliminarAmigo(request):
    if request.method == "POST":
        id_amigo = request.POST.get("idAmigo") #se obtiene el id desde el formulario    
        perfil = get_object_or_404(Perfil,user=request.user) #se obtiene el perfil del usuario que esta logueado
        amigo = get_object_or_404(User,id=id_amigo) #se obtiene al usuario desde el modelo User
        perfil.amigos.remove(amigo) #se elimina ese amigo del modelo 
        
    return redirect('mis-amigos')


@login_required
def verNovedades(request):
    if request.method == "GET":
        novedades = Novedades.objects.filter(user = request.user)
        novedades.update(leida = True)
        novedades= novedades.order_by('-fecha')
        return render(request,'novedades.html',{
            'novedades':novedades
        })
    
    
@login_required
def publicacion(request,idPost):
    post = get_object_or_404(Publicacion, id=idPost)
    return render(request,'publicacion.html',{
        'publicacion':post
    })
     
@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('ingreso')