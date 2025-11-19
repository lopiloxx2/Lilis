from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch


class PasswordChangeRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'userprofile'):
                if getattr(request.user.userprofile, 'must_change_password', False):
                    # Construir rutas permitidas. Usamos try/except por si alguna no está registrada.
                    try:
                        logout_url = reverse('logout')
                    except NoReverseMatch:
                        logout_url = '/logout/'
                    try:
                        pw_change_url = reverse('password_change')
                    except NoReverseMatch:
                        pw_change_url = '/accounts/password_change/'
                    try:
                        admin_index = reverse('admin:index')
                    except NoReverseMatch:
                        admin_index = '/admin/'
                    try:
                        login_url = reverse('login_registro')
                    except NoReverseMatch:
                        login_url = '/login/'

                    # Permitir acceso a las rutas de logout, cambio de contraseña, admin y login
                    allowed = (
                        request.path == logout_url or
                        request.path == pw_change_url or
                        request.path.startswith(admin_index) or
                        request.path.startswith(login_url)
                    )

                    if not allowed:
                        return redirect('password_change')

        return self.get_response(request)
