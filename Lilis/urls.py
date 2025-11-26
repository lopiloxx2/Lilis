from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('', include('productos.urls')),
    path('proveedores/', include('proveedores.urls')),
<<<<<<< HEAD
=======
    path('login/', include('login.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
>>>>>>> 86146f456b485dd03b4ef19c8fee35d8540bd50e
]
