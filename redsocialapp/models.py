from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, null=True)
    imagen = models.ImageField(upload_to='fotos_perfil/',default='default.png')
    descripcion = models.TextField(max_length=300, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #oneToOneField indica que la relacion entre el usuario y el perfil de 1 a 1, es decir, 1 usuario tiene 1 perfil.
    
    def __str__(self): #este metodo es para mostrar en el administrador de Django el username del usuario al que hace referencia el perfil.
        return self.user.username
    
class Publicacion(models.Model):
    imagen = imagen = models.ImageField(upload_to='publicaciones/')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=150)
    fechaPublicacion = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)]) #validators=[MinValueValidator(0)] es una validación que asegura que el valor del campo no sea menor que un mínimo especificado, en este caso, 0.