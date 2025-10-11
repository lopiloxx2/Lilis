from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Producto, Cliente, Venta, DetalleVenta
from .forms import ProductoForm
from .forms import VentaForm

def inicio(request):
    return render(request, 'productos/index.html')

def ver_productos(request):
    productos = Producto.objects.all()
    print("=== PRODUCTOS ENCONTRADOS ===")
    print(productos)
    for p in productos:
        print(p.nombre)
    return render(request, 'productos/productos.html', {'productos': productos})
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/productos.html', {'productos': productos})


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'productos/clientes.html', {'clientes': clientes})

def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'productos/ventas.html', {'ventas': ventas})
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Agregar Producto'})


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Editar Producto'})


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'productos/eliminar.html', {'producto': producto})


def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ventas')
    else:
        form = VentaForm()
    return render(request, 'productos/form_venta.html', {'form': form, 'titulo': 'Agregar Venta'})


def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('lista_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'productos/form_venta.html', {'form': form, 'titulo': 'Editar Venta'})


def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('lista_ventas')
    return render(request, 'productos/eliminar_venta.html', {'venta': venta})
