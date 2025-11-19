from django.db import models


class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_categoria


class Producto(models.Model):
    sku = models.CharField(max_length=191, unique=True)
    ean_upc = models.CharField(max_length=64, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)

    # Unidades y precios
    uom_compra = models.CharField(max_length=10, default='UN')
    uom_venta = models.CharField(max_length=10, default='UN')
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    costo_estandar = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    costo_promedio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    impuesto_iva = models.DecimalField(max_digits=5, decimal_places=2, default=19)

    # Stock y control
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    stock_maximo = models.IntegerField(null=True, blank=True)
    punto_reorden = models.IntegerField(null=True, blank=True)
    perishable = models.BooleanField(default=False)
    control_por_lote = models.BooleanField(default=False)
    control_por_serie = models.BooleanField(default=False)

    # Relaciones / soportes
    imagen_url = models.URLField(blank=True, null=True)
    ficha_tecnica_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

    @property
    def stock_actual(self):
        # Prefer sum of lotes if control_por_lote, otherwise stored stock
        try:
            if self.control_por_lote:
                total = self.lotes.aggregate(total=models.Sum('cantidad'))['total'] or 0
                return int(total)
        except Exception:
            pass
        return int(self.stock or 0)

    @property
    def alerta_bajo_stock(self):
        return self.stock_actual <= (self.stock_minimo or 0)

    @property
    def alerta_por_vencer(self):
        # Simple heuristic: any lote con vencimiento en menos de 30 días
        if not self.perishable:
            return False
        from django.utils import timezone
        from datetime import timedelta
        hoy = timezone.localdate()
        proximidad = hoy + timedelta(days=30)
        return self.lotes.filter(fecha_vencimiento__isnull=False, fecha_vencimiento__lte=proximidad).exists()


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

    # When True, user must change the auto-generated password at first login
    must_change_password = models.BooleanField(default=False)

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


# ---------- INVENTARIO (Módulo Transaccional) ----------
class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
    codigo_lote = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    proveedor = models.ForeignKey('proveedores.Proveedor', on_delete=models.SET_NULL, null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'codigo_lote')

    def __str__(self):
        return f"{self.producto.nombre} - {self.codigo_lote} ({self.cantidad})"


class InventoryMovement(models.Model):
    TIPO_MOVIMIENTO = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
        ('DEVOLUCION', 'Devolución'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=150, blank=True)  # username who performed
    proveedor = models.ForeignKey('proveedores.Proveedor', on_delete=models.SET_NULL, null=True, blank=True)
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_origen')
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_destino')
    referencia = models.CharField(max_length=200, blank=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha:%Y-%m-%d %H:%M}"


class MovementItem(models.Model):
    movimiento = models.ForeignKey(InventoryMovement, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
