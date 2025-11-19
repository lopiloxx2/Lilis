from django.contrib import admin
from .models import Categoria, Producto, Usuario, Venta, DetalleVenta
from .models import Bodega, Lote, InventoryMovement, MovementItem


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria',)
    search_fields = ('nombre_categoria',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'categoria', 'precio_venta', 'stock', 'marca')
    list_filter = ('categoria', 'marca')
    search_fields = ('nombre', 'sku')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nombres', 'apellidos', 'rol', 'estado')
    search_fields = ('username', 'email', 'nombres', 'apellidos')
    list_filter = ('rol', 'estado')


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'total')
    inlines = [DetalleVentaInline]


@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('producto', 'codigo_lote', 'cantidad', 'fecha_vencimiento', 'proveedor')
    list_filter = ('producto',)


class MovementItemInline(admin.TabularInline):
    model = MovementItem
    extra = 1


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'fecha', 'usuario', 'proveedor', 'bodega_origen', 'bodega_destino')
    inlines = [MovementItemInline]


@admin.register(MovementItem)
class MovementItemAdmin(admin.ModelAdmin):
    list_display = ('movimiento', 'producto', 'lote', 'cantidad', 'precio_unitario')
