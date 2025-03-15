from .models import Perfil
from django import forms

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'nombre', 'descripcion']