from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado, ConfiguracionUsuario, Curso

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UsuarioPersonalizado
        fields = ('username', 'email', 'rol', 'sobre_mi', 'foto_perfil', 'password1', 'password2')

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ('username', 'email', 'rol', 'sobre_mi', 'foto_perfil')

        widgets = {
            'sobre_mi': forms.Textarea(attrs={'rows':4}),
        }

class ConfsPerfilForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionUsuario
        fields = ['recibir_notificaciones', 'recibir_ofertas']
        widgets = {
            'recibir_notificaciones': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recibir_ofertas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre_curso', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

class InscripcionCursoForm(forms.Form):
    codigo_acceso = forms.CharField(label="Código de Curso", max_length=10, required=True)