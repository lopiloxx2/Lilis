from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validar_rut(rut):
    rut = rut.upper().replace(".", "").replace("-", "")
    cuerpo, dv = rut[:-1], rut[-1]

    suma = 0
    multiplo = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        # Ciclo de multiplicadores 2,3,4,5,6,7,2,3,...
        multiplo = 2 if multiplo == 7 else multiplo + 1

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

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    telefono = models.CharField(max_length=20, blank=True)
    empresa = models.CharField(max_length=100, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.rut})"