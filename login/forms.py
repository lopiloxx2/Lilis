from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario

class RegistroForm(forms.ModelForm):
    username = forms.CharField(label="Usuario", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    rut = forms.CharField(label="RUT", max_length=12, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label="Teléfono", max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    empresa = forms.CharField(label="Empresa", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PerfilUsuario
        fields = ['rut', 'telefono', 'empresa']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")