from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # PRODUCTOS
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # CLIENTES
    path('clientes/', views.lista_clientes, name='lista_clientes'),

    # VENTAS
    path('ventas/', views.lista_ventas, name='lista_ventas'),
]
