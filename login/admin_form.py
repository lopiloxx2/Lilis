from django import forms
from django.contrib.auth.models import User
from login.models import PerfilUsuario

class CustomUserCreationForm(forms.ModelForm):
    rut = forms.CharField(max_length=12, required=True, label="RUT")
    telefono = forms.CharField(max_length=20, required=False)
    empresa = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
