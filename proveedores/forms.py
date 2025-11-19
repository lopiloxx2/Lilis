# forms.py
from django import forms
from .models import Proveedor
from django.core.exceptions import ValidationError

def validar_rut(rut):
    rut = rut.upper().replace(".", "").replace("-", "")
    if not rut[:-1].isdigit():
        raise ValidationError("El cuerpo del RUT debe contener solo números.")
    
    cuerpo = rut[:-1]
    dv = rut[-1]

    suma = 0
    multiplo = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2

    resto = suma % 11
    digito = 11 - resto
    if digito == 11:
        digito = "0"
    elif digito == 10:
        digito = "K"
    else:
        digito = str(digito)

    if dv != digito:
        raise ValidationError("RUT inválido: dígito verificador incorrecto.")

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_rut(self):
        rut = self.cleaned_data.get('rut', '').strip()
        rut_sin_formato = rut.replace(".", "").replace("-", "").upper()
        validar_rut(rut_sin_formato)
        # Normalizar el RUT a formato sin puntos y con guion antes del dígito verificador
        cuerpo = rut_sin_formato[:-1]
        dv = rut_sin_formato[-1]
        normalized = f"{cuerpo}-{dv}"
        return normalized