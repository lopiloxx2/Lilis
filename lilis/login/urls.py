from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_registro_view, name='login_registro'),
   # path('logout/', LogoutView.as_view(next_page='login_registro'), name='logout'),
]