from .models import Perfil,Publicacion,Comentario
from django import forms

class PerfilFormCompleto(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'descripcion', 'nombre', 'apellido']
        
class PerfilFormReducido(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen','descripcion']
        
class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['imagen', 'descripcion']
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario']