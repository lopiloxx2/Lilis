# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from .forms import ProveedorForm
from django.db.models import Q
from django.core.paginator import Paginator
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse

def exportar_proveedores_excel(request):
    query = request.GET.get('q', '').strip()
    proveedores_qs = Proveedor.objects.all()

    if query:
        proveedores_qs = proveedores_qs.filter(
            Q(razon_social__icontains=query) |
            Q(rut__icontains=query)
        )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Proveedores"

    headers = ["RUT", "Razón Social", "Email", "Teléfono", "Ciudad"]
    ws.append(headers)

    for p in proveedores_qs.iterator():
        ws.append([p.rut, p.razon_social, p.email, p.telefono, p.ciudad])

    for i, h in enumerate(headers, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(12, len(h) + 2)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=proveedores.xlsx'
    wb.save(response)
    return response

def lista_proveedores(request):
    query = request.GET.get('q', '').strip()
    proveedores_qs = Proveedor.objects.all()

    if query:
        proveedores_qs = proveedores_qs.filter(
            Q(razon_social__icontains=query) |
            Q(rut__icontains=query)
        )

    paginator = Paginator(proveedores_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "query": query}

    if request.headers.get("HX-Request") == "true":
        return render(request, "proveedores/_grid.html", context)

    return render(request, "proveedores/lista.html", context)


# views.py
def crear_proveedor(request):
    if request.method == 'POST':
        print("Formulario recibido")
        form = ProveedorForm(request.POST)
        if form.is_valid():
            print("Formulario válido")
            form.save()
            return redirect('lista_proveedores')
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/formulario.html', {'form': form})

def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/formulario.html', {'form': form})

def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('lista_proveedores')
    return render(request, 'proveedores/eliminar_proveedor.html', {'proveedor': proveedor})

def test_form(request):
    if request.method == 'POST':
        print("Formulario recibido")  # Esto debe aparecer en consola
    return render(request, 'proveedores/test_form.html')