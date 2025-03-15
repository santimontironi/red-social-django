from .models import Perfil
from django import forms

class PerfilForm(forms.Form):
    class Meta:
        model = Perfil
        fields = ['nombre','imagen']