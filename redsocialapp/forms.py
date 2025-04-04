from .models import Perfil,Publicacion,Comentario
from django import forms

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'nombre', 'apellido', 'descripcion']
        
class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['imagen', 'descripcion']
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario']