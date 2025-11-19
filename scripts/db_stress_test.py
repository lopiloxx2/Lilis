"""
Script de prueba de estrés para la base de datos usando el ORM de Django.

Características:
- Usa el `Producto` (y `Categoria`) del app `productos`.
- Ejecuta operaciones concurrentes con `ThreadPoolExecutor`.
- Operaciones: crear, leer, actualizar, borrar.
- Por seguridad, sólo borra registros cuyo `sku` empiece con el prefijo configurado (por defecto `STRESS-`).

Uso (PowerShell):
    python scripts\db_stress_test.py --threads 20 --ops 1000 --prefix STRESS-

Notas:
- Ejecuta usando el Python/virtualenv del proyecto (el mismo que usas para `manage.py`).
- Asegúrate de que `DJANGO_SETTINGS_MODULE` apunte a `Lilis.settings` (el script lo configura automáticamente).
- No modifica modelos fuera de los prefijos indicados.
"""

import os
import sys
from pathlib import Path
import random
import string
import argparse
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Detectar automáticamente el directorio raíz del proyecto (donde está `manage.py`) y añadirlo a `sys.path`
file_path = Path(__file__).resolve()
project_root = None
for parent in file_path.parents:
    if (parent / 'manage.py').exists() or (parent / 'Lilis').is_dir():
        project_root = parent
        break
if project_root is None:
    # fallback razonable: subir 2 niveles
    project_root = file_path.parents[2] if len(file_path.parents) >= 3 else file_path.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lilis.settings')
import django
django.setup()

from django.db import transaction
from django.db.utils import IntegrityError
from productos.models import Producto, Categoria
from django.utils import timezone
from decimal import Decimal

lock = threading.Lock()

def gen_sku(prefix):
    suf = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}{suf}"


def seed_products(n, prefix):
    """Crea `n` productos con SKUs únicos que empiezan por `prefix`.
    Usa bulk_create para rendimiento.
    """
    # Obtener o crear la categoría; tolerar si hay duplicados existentes
    try:
        cat, _ = Categoria.objects.get_or_create(nombre_categoria='StressTest')
    except Categoria.MultipleObjectsReturned:
        qs = Categoria.objects.filter(nombre_categoria='StressTest')
        cat = qs.first()
        print(f"Warning: se encontraron {qs.count()} categorias 'StressTest'. Usando id={cat.id}.")
    objs = []
    batch_size = 1000
    created = 0
    for i in range(n):
        sku = gen_sku(prefix)
        precio = Decimal(str(round(random.uniform(1, 1000), 2)))
        stock = random.randint(0, 1000)
        p = Producto(
            sku=sku,
            nombre=f"Producto {sku}",
            descripcion='Pre-seed creado por script',
            categoria=cat,
            marca='MarcaStress',
            modelo=None,
            uom_compra='UN',
            uom_venta='UN',
            factor_conversion=Decimal('1'),
            costo_estandar=None,
            costo_promedio=None,
            precio_venta=precio,
            impuesto_iva=Decimal('19'),
            stock=stock,
            stock_minimo=0,
            perishable=False,
            control_por_lote=False,
            control_por_serie=False,
        )
        objs.append(p)
        # bulk insert in batches to avoid huge memory usage
        if len(objs) >= batch_size:
            Producto.objects.bulk_create(objs, batch_size=batch_size)
            created += len(objs)
            print(f"  Seeded {created}/{n}")
            objs = []
    if objs:
        Producto.objects.bulk_create(objs, batch_size=batch_size)
        created += len(objs)
        print(f"  Seeded {created}/{n}")
    print(f"Seed completo: {created} productos creados con prefijo '{prefix}'")
    # Mostrar cuántos productos con el prefijo existen ahora
    total_with_prefix = Producto.objects.filter(sku__startswith=prefix).count()
    print(f"Productos con prefijo '{prefix}' en BD: {total_with_prefix}")

def create_product(prefix):
    sku = gen_sku(prefix)
    try:
        with transaction.atomic():
            cat, _ = Categoria.objects.get_or_create(nombre_categoria='StressTest')
            p = Producto.objects.create(
                sku=sku,
                nombre=f"Producto {sku}",
                descripcion='Creado por script de stress test',
                categoria=cat,
                marca='MarcaStress',
                modelo=None,
                uom_compra='UN',
                uom_venta='UN',
                factor_conversion=Decimal('1'),
                costo_estandar=None,
                costo_promedio=None,
                precio_venta=Decimal(str(round(random.uniform(1, 1000),2))),
                impuesto_iva=Decimal('19'),
                stock=random.randint(0, 1000),
                stock_minimo=0,
                perishable=False,
                control_por_lote=False,
                control_por_serie=False,
            )
            return ('create', p.id)
    except IntegrityError:
        return ('create_fail', sku)

def read_product(prefix):
    # leer un producto al azar (dentro del prefijo si existe)
    qs = Producto.objects.filter(sku__startswith=prefix)
    count = qs.count()
    if count == 0:
        # fallback: leer cualquier producto
        qs = Producto.objects.all()
        count = qs.count()
        if count == 0:
            return ('read_none', None)
    idx = random.randrange(count)
    p = qs.all()[idx]
    # acceder a algunos campos
    _ = p.nombre
    _ = p.precio_venta
    return ('read', p.id)

def update_product(prefix):
    qs = Producto.objects.filter(sku__startswith=prefix)
    count = qs.count()
    if count == 0:
        return ('update_none', None)
    idx = random.randrange(count)
    with transaction.atomic():
        p = qs.all()[idx]
        # actualizar stock y precio
        p.stock = max(0, p.stock + random.randint(-10, 50))
        p.precio_venta = round(float(p.precio_venta) * random.uniform(0.95, 1.05), 2)
        p.save()
        return ('update', p.id)

def delete_product(prefix):
    qs = Producto.objects.filter(sku__startswith=prefix)
    count = qs.count()
    if count == 0:
        return ('delete_none', None)
    idx = random.randrange(count)
    with transaction.atomic():
        p = qs.all()[idx]
        pid = p.id
        p.delete()
        return ('delete', pid)

def worker(thread_id, ops, prefix, ratios):
    results = { 'create':0, 'read':0, 'update':0, 'delete':0, 'create_fail':0, 'read_none':0, 'update_none':0, 'delete_none':0 }
    ops_types = ['create', 'read', 'update', 'delete']
    weights = [ratios.get('create',25), ratios.get('read',50), ratios.get('update',15), ratios.get('delete',10)]
    for i in range(ops):
        op = random.choices(ops_types, weights=weights, k=1)[0]
        try:
            if op == 'create':
                r = create_product(prefix)
            elif op == 'read':
                r = read_product(prefix)
            elif op == 'update':
                r = update_product(prefix)
            else:
                r = delete_product(prefix)
            results[r[0]] = results.get(r[0], 0) + 1
        except Exception as e:
            # Registrar el error y continuar
            with lock:
                print(f"[Thread {thread_id}] Error en op {op}: {e}")
    return results


def merge_results(list_of_dicts):
    merged = {}
    for d in list_of_dicts:
        for k,v in d.items():
            merged[k] = merged.get(k,0) + v
    return merged


def main():
    parser = argparse.ArgumentParser(description='Stress test DB usando Django ORM (productos.Producto)')
    parser.add_argument('--threads', type=int, default=10, help='Número de hilos concurrentes')
    parser.add_argument('--ops', type=int, default=1000, help='Operaciones por hilo')
    parser.add_argument('--prefix', type=str, default='STRESS-', help='Prefijo SKU para los registros de prueba')
    parser.add_argument('--create-ratio', type=int, default=25, help='Porcentaje relativo para crear (por defecto 25)')
    parser.add_argument('--read-ratio', type=int, default=50, help='Porcentaje relativo para leer (por defecto 50)')
    parser.add_argument('--update-ratio', type=int, default=15, help='Porcentaje relativo para actualizar (por defecto 15)')
    parser.add_argument('--delete-ratio', type=int, default=10, help='Porcentaje relativo para borrar (por defecto 10)')
    parser.add_argument('--sleep', type=float, default=0.0, help='Esperar segundos entre operaciones en cada hilo (opcional)')
    parser.add_argument('--seed', type=int, default=0, help='Si >0: crea N productos con el prefijo y sale (útil para pre-seed)')

    args = parser.parse_args()

    # Si se pidió pre-seed, lo realizamos y salimos
    if args.seed and args.seed > 0:
        print(f"Iniciando seed de {args.seed} productos con prefijo '{args.prefix}'...")
        seed_products(args.seed, args.prefix)
        return

    ratios = {
        'create': args.create_ratio,
        'read': args.read_ratio,
        'update': args.update_ratio,
        'delete': args.delete_ratio,
    }

    total_ops = args.threads * args.ops
    print(f"Iniciando stress test: {args.threads} hilos x {args.ops} ops = {total_ops} operaciones")
    print(f"Prefijo SKU usado para los registros de prueba: {args.prefix}")
    start = time.time()

    results = []
    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = [ ex.submit(worker, tid, args.ops, args.prefix, ratios) for tid in range(args.threads) ]
        for f in as_completed(futures):
            results.append(f.result())
            if args.sleep and args.sleep>0:
                time.sleep(args.sleep)

    merged = merge_results(results)
    elapsed = time.time() - start

    print('\nResultados agregados:')
    for k,v in sorted(merged.items(), key=lambda x: x[0]):
        print(f"  {k}: {v}")
    print(f"Tiempo transcurrido: {elapsed:.2f} segundos")
    print('Prueba completada. Recuerda que sólo se eliminaron registros con el prefijo indicado.')

if __name__ == '__main__':
    main()
