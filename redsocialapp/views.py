from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import (
    PerfilFormCompleto,
    PerfilFormReducido,
    PublicacionForm,
    ComentarioForm,
)
from .models import Publicacion, Perfil, Novedades, Amigo
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random, secrets
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse


# Create your views here.
def ingreso(request):
    if (
        request.user.is_authenticated
    ):  # si la cookie del usuario está, se abre la app en inicio.
        return redirect("inicio")

    if request.method == "GET":
        return render(request, "ingreso.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]

        busquedaUsuario = User.objects.filter(
            Q(username=username) | Q(perfil__email=username)
        ).first()

        if busquedaUsuario:
            usuarioAutenticado = authenticate(
                request, username=busquedaUsuario.username, password=password
            )
            if usuarioAutenticado is None:
                return render(
                    request,
                    "ingreso.html",
                    {"errorCredenciales": "Usuario o contraseña no válidos."},
                )
            else:

                if request.POST.get("sessionActiva"):
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)

                # Si el usuario no tiene el perfil creado, redirigir a crear perfil
                perfil = busquedaUsuario.perfil
                if perfil:
                    if perfil.confirmado == False:
                        login(request, usuarioAutenticado)
                        return redirect("confirmar-usuario", user_id=perfil.user.id)
                    elif perfil.creado == False:
                        login(request, usuarioAutenticado)
                        return redirect("crear-perfil")
                    else:
                        login(request, usuarioAutenticado)
                        return redirect("inicio")
        else:
            return render(
                request,
                "ingreso.html",
                {"errorCredenciales": "Usuario o contraseña no válidos."},
            )


def registro(request):
    if request.method == "GET":
        return render(request, "registro.html")
    else:
        username = request.POST["username"]
        clave1 = request.POST["password1"]
        clave2 = request.POST["password2"]
        email = request.POST["email"]

        if clave1 != clave2:
            return render(
                request,
                "registro.html",
                {
                    "errorClavesNoIguales": "Las claves deben coincidir. Vuelva a intentarlo."
                },
            )
        try:
            usuario = User.objects.create_user(
                username=username, email=email, password=clave1
            )
            perfil = Perfil(user=usuario, email=email, confirmado=False)
            perfil.codigo_verificacion = random.randint(100000, 999999)
            perfil.save()

            send_mail(
                subject="Código de verificación",
                message=f"Hola {username}, tu codigo es: {perfil.codigo_verificacion}",
                from_email="santiimontironi@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )

            return redirect("confirmar-usuario", user_id=usuario.id)

        except IntegrityError:
            return render(
                request,
                "registro.html",
                {
                    "errorUsuarioExistente": "El nombre de usuario ya existe. Por favor elige otro."
                },
            )


def confirmarUsuario(request, user_id):
    if request.method == "GET":
        return render(request, "verificarUsuario.html")
    else:
        codigo = request.POST["codigo"]
        try:
            perfil = Perfil.objects.get(user__id=user_id)
            if int(perfil.codigo_verificacion) == int(codigo):
                perfil.confirmado = True
                perfil.save()
                login(request, perfil.user)
                return redirect("crear-perfil")
            else:
                return render(
                    request,
                    "verificarUsuario.html",
                    {
                        "errorCodigoIncorrecto": "El código ingresado es incorrecto. Por favor vuelva a intentarlo."
                    },
                )
        except (User.DoesNotExist, Perfil.DoesNotExist):
            return render(
                request,
                "verificarUsuario.html",
                {
                    "errorUsuarioNoExistente": "El usuario no existe. Por favor vuelva a intentarlo."
                },
            )


def enviarToken(request):
    if request.method == "POST":
        emailUsuario = request.POST["email"]
        usuario = User.objects.filter(
            Q(username=emailUsuario) | Q(perfil__email=emailUsuario)
        ).first()
        if usuario:

            token = secrets.token_urlsafe()  # se genera un token aleatorio

            usuario.perfil.token = token  # se le asigna al usuario su token
            usuario.perfil.token_created = (
                timezone.now()
            )  # se le asigna al usuario la fecha y hora del token creado
            usuario.perfil.save()

            # se genera la url para cambiar clave agregando el id del usuario y el token seguro
            url_cambio_clave = request.build_absolute_uri(
                reverse("cambiar-clave", args=[usuario.id]) + f"?token={token}"
            )

            send_mail(
                subject="Cambio de contraseña.",
                message=f"Hola {usuario.username}, has restablecido tu contraseña de SocialByte. Para cambiarla haz click en este enlace: \n{url_cambio_clave}",
                from_email="santiimontironi@gmail.com",
                recipient_list=[usuario.perfil.email],
                fail_silently=False,
            )
            return render(
                request,
                "ingreso.html",
                {
                    "mensajeExito": "Se ha enviado un correo electrónico a tu bandeja de entrada."
                },
            )
        else:
            return render(
                request,
                "ingreso.html",
                {
                    "errorEmailNoExistente": "El email o nombre de usuario ingresado no existe. Por favor vuelva a intentarlo."
                },
            )

    return render(request, "cambiarClave.html", {"usuario": usuario})


def cambiarClave(request, id):
    try:
        usuario = User.objects.get(id=id)
        tiempoLimite = usuario.perfil.token_created + timedelta(
            hours=1
        )  # se le suma una hora a la hora que fue creado el token
        ahora = timezone.now()  # horario actual
        if ahora > tiempoLimite:
            return render(
                request,
                "cambiarClave.html",
                {
                    "tokenExpirado": "El token de confirmación ha vencido, por favor vuelve a solicitarlo.",
                    "usuario": usuario,
                },
            )
        if request.method == "POST":
            inputCambiarClave = request.POST["claveNueva"]
            usuario.set_password(inputCambiarClave)
            usuario.perfil.token = None
            usuario.perfil.token_created = None
            usuario.save()
            return render(
                request,
                "cambiarClave.html",
                {
                    "cambioCorrecto": "Contraseña cambiada correctamente, ya puedes iniciar sesión nuevamente en: ",
                    "usuario": usuario,
                },
            )
        else:
            return render(request, "cambiarClave.html", {"usuario": usuario})
    except User.DoesNotExist:
        return render(
            request,
            "cambiarClave.html",
            {"usuarioNoExistente": "Error. El usuario correspondiente no es válido."},
        )


@login_required
def crearPerfil(request):
    perfil = Perfil.objects.filter(
        user=request.user
    ).first()  # se obtiene el primer perfil encontrado con el id del usuario
    if request.method == "POST":
        form = PerfilFormCompleto(
            request.POST, request.FILES, instance=perfil
        )  # instance=perfil se usa para editar el perfil existente
        form.save()  # se guarda el perfil
        perfil.creado = True
        perfil.save()
        return redirect("inicio")
    else:
        form = PerfilFormCompleto(
            instance=perfil
        )  # instance=perfil se usa para mostrar el formulario con los datos del perfil

    return render(request, "crearPerfil.html", {"form": form})


@login_required
def inicio(request):
    if request.method == "GET":

        publicaciones = (
            Publicacion.objects.filter(autor=request.user)
            | Publicacion.objects.filter(
                autor__in=Amigo.objects.filter(
                    solicitante=request.user, aceptado=True
                ).values("receptor")
            )
            | Publicacion.objects.filter(
                autor__in=Amigo.objects.filter(
                    receptor=request.user, aceptado=True
                ).values("solicitante")
            )
        ).order_by("-fechaPublicacion")

        if publicaciones.exists():
            return render(request, "inicio.html", {"publicaciones": publicaciones})
        else:
            return render(request, "inicio.html", {"noHayPublicaciones": True})


@login_required
def agregarPublicacion(request):
    if request.method == "GET":
        formPublicacion = PublicacionForm()
        return render(
            request, "agregarPublicacion.html", {"formPublicacion": formPublicacion}
        )
    else:
        formPublicacion = PublicacionForm(request.POST, request.FILES)
        nuevaPublicacion = formPublicacion.save(commit=False)
        nuevaPublicacion.autor = request.user
        nuevaPublicacion.save()
        return redirect("inicio")


@login_required
def agregarMeGusta(request, id_post):
    publicacion = get_object_or_404(Publicacion, id=id_post)

    if request.method == "POST":
        liked = False

        if request.user in publicacion.liked_by.all():
            publicacion.liked_by.remove(request.user)
            publicacion.likes -= 1
        else:
            publicacion.liked_by.add(request.user)
            publicacion.likes += 1
            liked = True

            # Crear novedad solo si el autor de la publicación no es quien dio like
            if publicacion.autor != request.user:
                novedad = Novedades(
                    user=publicacion.autor,
                    novedad=f"El usuario {request.user.username} le ha dado me gusta a tu publicación",
                    tipo='like',
                    usuario=request.user,
                    post=publicacion,
                    leida=False,
                    aceptada=False
                )
                novedad.save()

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
    if request.method == "POST":
        idPublicacion = request.POST.get("publicacion_id")
        publicacion = Publicacion.objects.get(id=idPublicacion)

        formularioComentario = ComentarioForm(request.POST)
        if formularioComentario.is_valid():
            comentarioRealizado = formularioComentario.save(commit=False)
            comentarioRealizado.autor = request.user
            comentarioRealizado.publicacion = publicacion
            comentarioRealizado.save()

            publicacion.cantidadComentarios += 1
            publicacion.save()

            # Crear novedad solo si el autor de la publicación no es quien comenta
            if publicacion.autor != request.user:
                novedades = Novedades(
                    user=publicacion.autor,
                    novedad=f"El usuario {request.user.username} ha comentado tu foto.",
                    tipo='comentario',
                    usuario=request.user,
                    comentario=comentarioRealizado.text,  # Guarda solo el texto del comentario
                    post=publicacion,
                    leida=False,
                    aceptada=False
                )
                novedades.save()

            html = render_to_string(
                "comentarios.html", {"publicacion": publicacion}, request=request
            )
            return HttpResponse(html)
        else:
            # Si el formulario no es válido, puedes devolver un error o renderizar de nuevo
            return HttpResponse("Formulario inválido", status=400)
    else:
        formularioComentario = ComentarioForm()
        return render(request, "inicio.html", {"formComentario": formularioComentario})


@login_required
def miPerfil(request):
    perfil = request.user.perfil
    if request.method == "GET":
        cantidadPublicaciones = Publicacion.objects.filter(autor=request.user).count()
        formularioPerfil = PerfilFormReducido(instance=perfil)
        misPublicaciones = Publicacion.objects.filter(autor=request.user)
        
        amigos = User.objects.filter(
            Q(
                id__in=Amigo.objects.filter(
                    solicitante=request.user, aceptado=True
                ).values("receptor")
            )
            | Q(
                id__in=Amigo.objects.filter(
                    receptor=request.user, aceptado=True
                ).values("solicitante")
            )
        ).distinct()

        cantidadAmigos = amigos.count()

        return render(
            request,
            "miPerfil.html",
            {
                "form": formularioPerfil,
                "cantidadPublicaciones": cantidadPublicaciones,
                "misPublicaciones": misPublicaciones,
                "cantidadAmigos": cantidadAmigos
            },
        )
    else:
        formularioPerfil = PerfilFormReducido(
            request.POST, request.FILES, instance=perfil
        )
        perfilEditado = formularioPerfil.save(commit=False)
        perfilEditado.user = request.user
        perfilEditado.save()
        return redirect("mi-perfil")


@login_required
def buscarUsuarios(request):
    if request.method == "POST":
        busqueda = request.POST["buscador"]
        usuarios = Perfil.objects.filter(
            Q(nombre__icontains=busqueda)
            | Q(apellido__icontains=busqueda)
            | Q(user__username__icontains=busqueda)
        )
        if usuarios.exists():
            return render(request, "usuarios.html", {"usuarios": usuarios})
        else:
            return render(
                request,
                "usuarios.html",
                {
                    "usuariosNoEncontrados": "No hay usuarios con ese nombre. Vuelva a intentarlo."
                },
            )

    return render(request, "usuarios.html")


@login_required
def verUsuario(request, id_usuario):
    usuario = get_object_or_404(Perfil, id=id_usuario)
    publicaciones = Publicacion.objects.filter(autor=usuario.user)
    totalPublicaciones = Publicacion.objects.filter(autor=usuario.user).count()
    
    totalAmigos = Amigo.objects.filter(
        Q(solicitante=usuario.user, aceptado=True)
        | Q(receptor=usuario.user, aceptado=True)
    ).count()
    
    esAmigo = Amigo.objects.filter(
        (Q(solicitante=request.user, receptor=usuario.user) |
         Q(receptor=request.user, solicitante=usuario.user)),
        aceptado=True
    ).exists()
    
    if publicaciones:
        return render(
            request,
            "usuario.html",
            {
                "usuario": usuario,
                "publicaciones": publicaciones,
                "totalPublicaciones": totalPublicaciones,
                "totalAmigos": totalAmigos,
                "esAmigo": esAmigo
            },
        )
    else:
        noHayPublicaciones = "Este usuario aún no tiene publicaciones."
        return render(
            request,
            "usuario.html",
            {
                "usuario": usuario,
                "noHayPublicaciones": noHayPublicaciones,
                "totalAmigos": totalAmigos,
                "totalPublicaciones": totalPublicaciones,
                "esAmigo": esAmigo
            },
        )


@login_required
def misAmigos(request):
    amigos = User.objects.filter(
        Q(
            id__in=Amigo.objects.filter(
                solicitante=request.user, aceptado=True
            ).values("receptor")
        )
        | Q(
            id__in=Amigo.objects.filter(
                receptor=request.user, aceptado=True
            ).values("solicitante")
        )
    ).distinct()

    cantidadAmigos = amigos.count()

    return render(
        request,
        "misAmigos.html",
        {
            "amigos": amigos,
            "hayAmigos": cantidadAmigos > 0,
            "cantidadAmigos": cantidadAmigos,
        },
    )


@login_required
def buscarAmigos(request):
    if request.method == "POST":
        busqueda = request.POST.get("buscadorAmigos", "").strip()

        amigos = User.objects.filter(
            Q(
                id__in=Amigo.objects.filter(
                    solicitante=request.user, aceptado=True
                ).values("receptor")
            )
            | Q(
                id__in=Amigo.objects.filter(
                    receptor=request.user, aceptado=True
                ).values("solicitante")
            )
        )

        amigos_filtrados = amigos.filter(
            Q(username__icontains=busqueda)
            | Q(perfil__nombre__icontains=busqueda)
            | Q(perfil__apellido__icontains=busqueda)
        )

        cantidadAmigos = amigos.count()

        if amigos_filtrados.exists():
            return render(
                request,
                "misAmigos.html",
                {
                    "hayAmigos": True,
                    "amigos": amigos_filtrados,
                    "cantidadAmigos": cantidadAmigos,
                },
            )
        else:
            return render(
                request,
                "misAmigos.html",
                {"hayAmigos": False, "cantidadAmigos": cantidadAmigos},
            )

    return redirect("mis-amigos")

@login_required
def agregarAmigos(request):
    if request.method == "POST":
        id_receptor = request.POST.get("id_usuario")
        receptor = get_object_or_404(User, id=id_receptor)

        # Verificar si ya existe una solicitud pendiente
        existe_solicitud = Novedades.objects.filter(
            user=receptor,
            usuario=request.user,
            tipo="amigo",
            aceptada=False
        ).exists()

        if existe_solicitud:
            return HttpResponse("Ya enviaste una solicitud a este usuario.")

        Amigo.objects.create(
            solicitante=request.user,
            receptor=receptor,
            aceptado=False
        )

        Novedades.objects.create(
            user=receptor,
            usuario=request.user,
            novedad=f"{request.user.username} te ha enviado una solicitud de amistad.",
            tipo="amigo",
        )

        return HttpResponse("Solicitud de amistad enviada.")

@login_required
def responderSolicitudAmistad(request, id_novedad):
    solicitud = get_object_or_404(
        Novedades,
        id=id_novedad,
        user=request.user,
        tipo="amigo",
        aceptada=False
    )

    if request.method == "POST":
        accion = request.POST.get("accion")

        amistad = Amigo.objects.filter(
            solicitante=solicitud.usuario,
            receptor=request.user
        ).first()

        if accion == "aceptar":
            solicitud.aceptada = True
            solicitud.save()

            if amistad:
                amistad.aceptado = True
                amistad.save()

            # HTMX elimina la tarjeta
            return HttpResponse("")

        elif accion == "rechazar":
            if amistad:
                amistad.delete()
            solicitud.delete()
            return HttpResponse("")

        return HttpResponse("Acción inválida.", status=400)

    return HttpResponse("Método no permitido.", status=405)

@login_required
def eliminarAmigo(request):
    if request.method == "POST":
        id_amigo = request.POST.get("idAmigo")
        amigo = get_object_or_404(User, id=id_amigo)

        # se busca la relación de amistad (en cualquier sentido)
        relacion = Amigo.objects.filter(
            Q(solicitante=request.user, receptor=amigo)
            | Q(solicitante=amigo, receptor=request.user),
            aceptado=True,
        ).first()

        # Si existe la amistad, eliminarla
        if relacion:
            relacion.delete()

    return redirect("mis-amigos")

@login_required
def verNovedades(request):
    novedades = Novedades.objects.filter(user=request.user).order_by("-fecha")

    solicitudes_pendientes = novedades.filter(tipo="amigo", aceptada=False)
    otras_novedades = novedades.exclude(tipo="amigo")

    # Marcar todas como leídas
    novedades.update(leida=True)

    return render(
        request,
        "novedades.html",
        {
            "solicitudes_pendientes": solicitudes_pendientes,
            "novedades": otras_novedades,
        },
    )
    
@login_required
def publicacion(request, idPost):
    post = get_object_or_404(Publicacion, id=idPost)
    return render(request, "publicacion.html", {"publicacion": post})

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect("ingreso")
