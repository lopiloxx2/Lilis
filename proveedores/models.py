# models.py
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Validador para números
solo_numeros = RegexValidator(r'^[0-9]+$', 'Solo se permiten números.')

# Validador personalizado para RUT chileno
def validar_rut(rut):
    rut = rut.upper().replace(".", "").replace("-", "")
    if not rut[:-1].isdigit():
        raise ValidationError("El cuerpo del RUT debe contener solo números.")
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
        raise ValidationError("El RUT ingresado no es válido.")

class Proveedor(models.Model):
    rut = models.CharField(max_length=15, blank=False, null=False)
    razon_social = models.CharField(max_length=255, blank=False, null=False)
    nombre_fantasia = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True, validators=[solo_numeros])
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    plazos_pago = models.CharField(max_length=50, help_text="Ej: 30 días")
    moneda = models.CharField(max_length=10, default="CLP")
    descuentos = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    costo_promedio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lead_time = models.IntegerField(help_text="Días de entrega", null=True, blank=True)
    proveedor_preferente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.razon_social} ({self.rut})"
