from .models import Perfil,Publicacion
from django import forms

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'nombre', 'apellido', 'descripcion']
        
class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['imagen', 'descripcion']