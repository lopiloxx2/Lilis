from django import forms
from .models import Producto, Venta, Usuario
from django import forms

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'descripcion', 'precio_venta', 'stock', 'marca', 'categoria']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['total']
        widgets = {
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'nombres', 'apellidos', 'telefono',
            'rol', 'estado', 'mfa_habilitado', 'area', 'observaciones'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'mfa_habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
