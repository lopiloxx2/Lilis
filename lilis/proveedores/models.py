from django.db import models
from django.core.validators import RegexValidator

solo_numeros = RegexValidator(r'^[0-9]+$', 'Solo se permiten números.')

class Proveedor(models.Model):
    # Identificación
    rut = models.CharField(max_length=12, validators=[solo_numeros])
    telefono = models.CharField(max_length=15, blank=True, null=True, validators=[solo_numeros])
    nombre_fantasia = models.CharField(max_length=255, blank=True, null=True)

    # Contacto
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)

    # Condiciones comerciales
    plazos_pago = models.CharField(max_length=50, help_text="Ej: 30 días")
    moneda = models.CharField(max_length=10, default="CLP")
    descuentos = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    # Relación con productos
    proveedor_preferente = models.BooleanField(default=False)
    costo_promedio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lead_time = models.IntegerField(help_text="Días de entrega", null=True, blank=True)

    def __str__(self):
        return f"{self.razon_social} ({self.rut})"
