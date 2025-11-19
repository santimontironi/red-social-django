"""
URL configuration for redsocialproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from redsocialapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ingreso, name='ingreso'),
    path('cambiar-clave/<int:id>',views.cambiarClave,name='cambiar-clave'),
    path('enviar-token/',views.enviarToken,name='enviar-token'),
    path('registro/', views.registro, name='registro'),
    path('confirmar-usuario/<int:user_id>', views.confirmarUsuario, name='confirmar-usuario'),
    path('inicio/',views.inicio,name='inicio'),
    path('crear-perfil/',views.crearPerfil, name='crear-perfil'),
    path('agregar-publicacion/',views.agregarPublicacion, name='agregar-publicacion'),
    path('eliminar-publicacion/',views.eliminarPublicacion,name='eliminar_publicacion'),
    path('me-gusta/<int:id_post>',views.agregarMeGusta,name='me_gusta'),
    path('agregar-comentario/',views.agregarComentario, name='agregar-comentario'),
    path('mi-perfil/',views.miPerfil,name='mi-perfil'),
    path('usuarios/',views.buscarUsuarios,name='usuarios'),
    path('agregar-amigos/',views.agregarAmigos,name='agregar-amigos'),
    path('responder-solicitud/<int:id_novedad>/', views.responderSolicitudAmistad, name='responder-solicitud-amistad'),
    path('usuario/<int:id_usuario>',views.verUsuario,name='usuario'),
    path('mis-amigos/',views.misAmigos,name='mis-amigos'),
    path('buscar-amigos/',views.buscarAmigos,name='buscar-amigos'),
    path('eliminar-amigo/',views.eliminarAmigo,name='eliminar-amigo'),
    path('novedades/',views.verNovedades,name='novedades'),
    path('publicacion/<int:idPost>',views.publicacion,name='publicacion'),
    path('cerrar-sesion/',views.cerrarSesion,name='cerrar-sesion')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)