"""Script to fix existing Producto rows so they comply with the new model fields.

Run from the project root with:
    python scripts\fix_products.py

It will:
 - create a default category 'Sin categoría' if missing
 - fill null/blank fields with sensible defaults
 - report counts of updated rows
"""
import os
import sys
from pathlib import Path

# Locate project root (where manage.py lives)
file_path = Path(__file__).resolve()
project_root = None
for parent in file_path.parents:
    if (parent / 'manage.py').exists() or (parent / 'Lilis').is_dir():
        project_root = parent
        break
if project_root is None:
    project_root = file_path.parents[1]
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lilis.settings')
import django
django.setup()

from productos.models import Producto, Categoria
from django.db import transaction
from decimal import Decimal


def fix_products():
    cat, _ = Categoria.objects.get_or_create(nombre_categoria='Sin categoría')

    total = Producto.objects.count()
    updated = 0
    with transaction.atomic():
        for p in Producto.objects.all():
            changed = False
            if p.categoria is None:
                p.categoria = cat
                changed = True
            if not p.uom_compra:
                p.uom_compra = 'UN'
                changed = True
            if not p.uom_venta:
                p.uom_venta = 'UN'
                changed = True
            if not p.factor_conversion:
                p.factor_conversion = Decimal('1')
                changed = True
            if p.impuesto_iva is None:
                p.impuesto_iva = Decimal('19')
                changed = True
            if p.stock_minimo is None:
                p.stock_minimo = 0
                changed = True
            # Ensure boolean defaults
            if p.perishable is None:
                p.perishable = False
                changed = True
            if p.control_por_lote is None:
                p.control_por_lote = False
                changed = True
            if p.control_por_serie is None:
                p.control_por_serie = False
                changed = True
            # Precio and stock fallbacks
            if p.precio_venta is None:
                p.precio_venta = Decimal('0')
                changed = True
            if p.stock is None:
                p.stock = 0
                changed = True

            if changed:
                p.save()
                updated += 1

    print(f"Productos totales: {total}; actualizados: {updated}")


if __name__ == '__main__':
    fix_products()
