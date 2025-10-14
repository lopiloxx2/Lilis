from django import forms
from .models import Proveedor

def validar_rut(rut):
    rut = rut.upper().replace(".", "").replace("-", "")
    cuerpo, dv = rut[:-1], rut[-1]

    suma = 0
    multiplo = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = 9 if multiplo == 7 else multiplo + 1

    resto = suma % 11
    digito = 11 - resto
    if digito == 11:
        digito = "0"
    elif digito == 10:
        digito = "K"
    else:
        digito = str(digito)

    if dv != digito:
        raise forms.ValidationError("El RUT ingresado no es válido.")

class ProveedorForm(forms.ModelForm):
    rut = forms.CharField(validators=[validar_rut])

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
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
