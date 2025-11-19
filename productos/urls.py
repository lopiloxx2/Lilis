from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    # INVENTARIO
    path('inventario/', views.inventory_list, name='inventory_list'),
    path('inventario/<int:pk>/', views.inventory_detail, name='inventory_detail'),

    # PRODUCTOS
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/stress-load/', views.bulk_create_productos, name='bulk_create_productos'),
    path('productos/stress-clear/', views.bulk_delete_productos, name='bulk_delete_productos'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/exportar/', views.exportar_productos_excel, name='exportar_productos_excel'),


    # USUARIOS
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/exportar/', views.exportar_usuarios_excel, name='exportar_usuarios_excel'),
    path('usuarios/nuevo/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/confirmacion/', views.usuario_confirmacion, name='usuario_confirmacion'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/reset-password/<int:pk>/', views.admin_reset_password, name='admin_reset_password'),




    # VENTAS
    # Reuse the ventas URL to show the Inventory module (requested)
    path('ventas/', views.inventory_list, name='lista_ventas'),
    path('ventas/exportar/', views.exportar_ventas_excel, name='exportar_ventas_excel'),
]
