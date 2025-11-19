from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('productos.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('login/', include('login.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
