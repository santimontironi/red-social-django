from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, null=True)
    imagen = models.ImageField(upload_to='fotos_perfil/')
    descripcion = models.TextField(max_length=300, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #oneToOneField indica que la relacion entre el usuario y el perfil de 1 a 1, es decir, 1 usuario tiene 1 perfil.
    amigos = models.ManyToManyField(User,blank=True,related_name='amigos')

class Publicacion(models.Model):
    imagen = models.ImageField(upload_to='publicaciones/')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=150)
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)]) #validators=[MinValueValidator(0)] es una validación que asegura que el valor del campo no sea menor que un mínimo especificado, en este caso, 0.
    liked_by = models.ManyToManyField(User, related_name='likes', blank=True) #Cada usuario puede dar "Me gusta" a múltiples publicaciones, y cada publicación puede recibir "Me gusta" de múltiples usuarios.