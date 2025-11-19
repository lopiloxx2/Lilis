from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from productos.models import Usuario as AppUsuario

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            # Superuser can access everything
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            try:
                app_user = AppUsuario.objects.get(username=request.user.username)
            except AppUsuario.DoesNotExist:
                # If the application-level user is missing, inform the user and
                # redirect to logout so an administrator can fix the account.
                # Returning a silent redirect to a login-protected page caused
                # confusion where templates showed the login link unexpectedly.
                messages.error(request, 'Usuario de la aplicación no encontrado. Contacte al administrador.')
                return redirect('logout')

            # If the user must change temporary password, force them to the change page
            if getattr(app_user, 'must_change_password', False):
                messages.info(request, 'Debe cambiar su contraseña temporal antes de continuar.')
                return redirect('change_password')

            if app_user.rol in allowed_roles:
                return view_func(request, *args, **kwargs)

            return redirect('inicio')

        return _wrapped
    return decorator
