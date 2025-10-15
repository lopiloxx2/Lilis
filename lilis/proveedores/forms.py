from django import forms
from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'pattern': '[0-9Kk]+',
                'title': 'Ingrese solo números y K si corresponde'
            }),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'plazos_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'moneda': forms.TextInput(attrs={'class': 'form-control'}),
            'descuentos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'proveedor_preferente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'costo_promedio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'lead_time': forms.NumberInput(attrs={'class': 'form-control'}),
        }
