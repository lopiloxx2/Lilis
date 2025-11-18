from django.contrib import admin
from .models import Categoria, Producto, Usuario, Venta, DetalleVenta


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
