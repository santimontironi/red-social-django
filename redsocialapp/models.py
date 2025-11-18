from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Perfil(models.Model):
    email = models.EmailField(unique=True) #El campo email es único, lo que significa que no puede haber dos usuarios con el mismo correo electrónico en la base de datos.
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, null=True)
    token = models.CharField(max_length=200,null=True, blank=True)
    token_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    imagen = models.ImageField(upload_to='fotos_perfil/')
    descripcion = models.TextField(max_length=300, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False,blank=False)
    codigo_verificacion = models.CharField(max_length=6, blank=True, null=True)
    creado = models.BooleanField(default=False)
    
class Publicacion(models.Model):
    imagen = models.ImageField(upload_to='publicaciones/')
    autor = models.ForeignKey(User,on_delete=models.CASCADE, related_name='publicacion')
    descripcion = models.TextField(max_length=150, blank=True)
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)]) #validators=[MinValueValidator(0)] es una validación que asegura que el valor del campo no sea menor que un mínimo especificado, en este caso, 0.
    liked_by = models.ManyToManyField(User, related_name='likes', blank=True) #Cada usuario puede dar "Me gusta" a múltiples publicaciones, y cada publicación puede recibir "Me gusta" de múltiples usuarios.
    cantidadComentarios = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE,related_name='comentario')
    comentario = models.TextField(max_length=150)
    fechaComentario = models.DateTimeField(auto_now_add=True)
    
class Novedades(models.Model):
    TIPO_NOVEDAD = [
        ('like', 'Me gusta'),
        ('comentario', 'Comentario'),
        ('amigo', 'Solicitud de amistad'),
        ('sistema', 'Sistema'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarioPertenecienteNovedad')
    novedad = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_NOVEDAD, default='sistema')
    fecha = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    post = models.ForeignKey('Publicacion', null=True, blank=True, on_delete=models.SET_NULL, related_name='nuevoAmigo')

    comentario = models.TextField(max_length=150, null=True, blank=True)

    leida = models.BooleanField(default=False, null=True, blank=True)
    aceptada = models.BooleanField(default=False, null=True, blank=True)

class Amigo(models.Model):
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amigos_enviados')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amigos_recibidos')
    aceptado = models.BooleanField(default=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    
    #se define una restricción única compuesta en esos dos campos.
    class Meta:
        unique_together = ('solicitante','receptor')