from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_registro_view, name='login_registro'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('forgot/', views.forgot_password_view, name='forgot_password'),
    path('reset/<str:uidb64>/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
]