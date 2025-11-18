from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def login_registro_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido, {user.username}")
                return redirect('dashboard')  # Cambia esto por tu vista principal
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")

        elif action == 'registro':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, "Las contraseñas no coinciden.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "El nombre de usuario ya está en uso.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                login(request, user)
                messages.success(request, "Registro exitoso.")
                return redirect('dashboard')

    return render(request, 'login/login.html')