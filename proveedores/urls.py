# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_proveedores, name='lista_proveedores'),
    path('nuevo/', views.crear_proveedor, name='crear_proveedor'),
    path('editar/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('test/', views.test_form, name='test_form'),
    path('exportar/', views.exportar_proveedores_excel, name='exportar_proveedores_excel'),
]
