from django.db import models
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_categoria


class Producto(models.Model):
    sku = models.CharField(max_length=191, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    # Stock mínimo requerido al crear un producto: 1
    stock = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    marca = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"


class Usuario(models.Model):
    ESTADOS = [("ACTIVO", "Activo"), ("INACTIVO", "Inactivo")]
    ROLES = [("ADMIN", "Administrador"), ("VENDEDOR", "Vendedor"), ("CAJA", "Caja")]

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=191, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    rol = models.CharField(max_length=20, choices=ROLES)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="ACTIVO")
    mfa_habilitado = models.BooleanField(default=False)

    password = models.CharField(max_length=128, default="")  

    ultimo_acceso = models.DateTimeField(blank=True, null=True)
    sesiones_activas = models.PositiveIntegerField(default=0)

    area = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.username})"



class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta #{self.id} - {self.total}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
