from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Producto, Usuario, Venta, DetalleVenta
from .forms import ProductoForm
from .forms import VentaForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
import openpyxl
from openpyxl.utils import get_column_letter
from .forms import UsuarioForm 
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
import secrets
import string

def inicio(request):
    return render(request, 'productos/index.html')

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})

def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})

def exportar_productos_excel(request):
    query = request.GET.get('q', '').strip()
    productos_qs = Producto.objects.select_related("categoria").all()

    if query:
        productos_qs = productos_qs.filter(
            Q(nombre__icontains=query) |
            Q(sku__icontains=query) |
            Q(marca__icontains=query)
        )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Productos"

    headers = ["SKU", "Nombre", "Categoría", "Precio", "Stock", "Marca"]
    ws.append(headers)

    for p in productos_qs.iterator():
        ws.append([
            p.sku,
            p.nombre,
            p.categoria.nombre_categoria if p.categoria else "",
            float(p.precio_venta),
            p.stock,
            p.marca or ""
        ])

    for i, h in enumerate(headers, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(12, len(h) + 2)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=productos.xlsx'
    wb.save(response)
    return response

def ver_productos(request):
    productos = Producto.objects.all()
    print("=== PRODUCTOS ENCONTRADOS ===")
    print(productos)
    for p in productos:
        print(p.nombre)
    return render(request, 'productos/productos.html', {'productos': productos})


def lista_productos(request):
    query = request.GET.get('q', '').strip()
    productos_qs = Producto.objects.select_related("categoria").all()

    if query:
        productos_qs = productos_qs.filter(
            Q(nombre__icontains=query) |
            Q(sku__icontains=query) |
            Q(marca__icontains=query)
        )

    paginator = Paginator(productos_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "query": query}

    if request.headers.get("HX-Request") == "true":
        return render(request, "productos/_grid.html", context)

    return render(request, "productos/productos.html", context)


def lista_usuarios(request):
    query = request.GET.get('q', '').strip()
    usuarios_qs = Usuario.objects.all()

    if query:
        usuarios_qs = usuarios_qs.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(telefono__icontains=query)
        )

    paginator = Paginator(usuarios_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "query": query}

    if request.headers.get("HX-Request") == "true":
        return render(request, "usuarios/_grid_usuarios.html", context)

    return render(request, "usuarios/usuarios.html", context)

def exportar_usuarios_excel(request):
    query = request.GET.get('q', '').strip()
    usuarios_qs = Usuario.objects.all()

    if query:
        usuarios_qs = usuarios_qs.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(telefono__icontains=query)
        )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Usuarios"

    headers = ["Username", "Email", "Nombres", "Apellidos", "Teléfono", "Rol", "Estado"]
    ws.append(headers)

    for u in usuarios_qs.iterator():
        ws.append([
            u.username,
            u.email,
            u.nombres,
            u.apellidos,
            u.telefono or "",
            u.rol,
            u.estado
        ])

    for i, h in enumerate(headers, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(12, len(h) + 2)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=usuarios.xlsx'
    wb.save(response)
    return response

def generar_contrasena(longitud=10):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))


#USUARIOS
def generar_contrasena(longitud=10):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Generar contraseña aleatoria
            contrasena = generar_contrasena()
            usuario.password = make_password(contrasena)
            usuario.save()
            # Mostrar pantalla de confirmación con la contraseña generada
            return render(request, 'usuarios/confirmacion_usuario.html', {
                'usuario': usuario,
                'contrasena': contrasena
            })
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})

#PRODUCTOS
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
#VENTAS
def lista_ventas(request):
    query = request.GET.get('q', '').strip()
    ventas_qs = Venta.objects.all().order_by('-fecha')

    if query:
        ventas_qs = ventas_qs.filter(
            Q(id__icontains=query) |
            Q(fecha__icontains=query) |
            Q(total__icontains=query)
        )

    paginator = Paginator(ventas_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "query": query}

    if request.headers.get("HX-Request") == "true":
        return render(request, "ventas/_grid_ventas.html", context)

    return render(request, "ventas/ventas.html", context)

def exportar_ventas_excel(request):

    query = request.GET.get('q', '').strip()
    ventas_qs = Venta.objects.all().order_by('-fecha')

    if query:
        ventas_qs = ventas_qs.filter(
            Q(id__icontains=query) |
            Q(fecha__icontains=query) |
            Q(total__icontains=query)
        )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ventas"

    headers = ["ID", "Fecha", "Total"]
    ws.append(headers)

    for v in ventas_qs.iterator():
        ws.append([v.id, v.fecha.strftime("%Y-%m-%d %H:%M"), v.total])

    for i, h in enumerate(headers, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(12, len(h) + 2)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=ventas.xlsx'
    wb.save(response)
    return response

# NO SE USAN
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
