from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='fotos_perfil/',default='default.png')
    descripcion = models.TextField(max_length=300, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #oneToOneField indica que la relacion entre el usuario y el perfil de 1 a 1, es decir, 1 usuario tiene 1 perfil.
    
    def __str__(self): #este metodo es para mostrar en el administrador de Django el username del usuario al que hace referencia el perfil.
        return self.user.username