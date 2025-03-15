from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='fotos_perfil/',default='default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE) #oneToOneField indica que la relacion entre el usuario y el perfil de 1 a 1, es decir, 1 usuario tiene 1 perfil.