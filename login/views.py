from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from productos.models import Usuario as AppUsuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
import logging
import smtplib
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from Lilis.auth_utils import validate_password_policy


def logout_view(request):
    logout(request)
    return redirect('login_registro')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        if not p1 or not p2:
            messages.error(request, 'Ambas contraseñas son obligatorias.')
        elif p1 != p2:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            ok, msg = validate_password_policy(p1)
            if not ok:
                messages.error(request, msg)
                return render(request, 'login/change_password.html')

            # actualizar auth.User
            user = request.user
            user.set_password(p1)
            user.save()

            # actualizar productos.Usuario
            try:
                app_user = AppUsuario.objects.get(username=user.username)
                app_user.password = make_password(p1)
                app_user.must_change_password = False
                app_user.save()
            except AppUsuario.DoesNotExist:
                pass

            # re-login user with new password
            user = authenticate(request, username=user.username, password=p1)
            if user is not None:
                login(request, user)

            messages.success(request, 'Contraseña actualizada correctamente.')
            # redirect depending on role
            try:
                app_user = AppUsuario.objects.get(username=request.user.username)
                if request.user.is_superuser or app_user.rol == 'ADMIN':
                    return redirect('inicio')
                else:
                    return redirect('lista_productos')
            except AppUsuario.DoesNotExist:
                return redirect('lista_productos')

    return render(request, 'login/change_password.html')


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
                # Si es superuser, tratarlo como administrador de la app
                # y redirigir a la página principal de la aplicación
                # Buscar rol en la tabla de la app
                try:
                    app_user = AppUsuario.objects.get(username=user.username)
                    # If must change password, redirect to change password page
                    if getattr(app_user, 'must_change_password', False):
                        return redirect('change_password')

                    if user.is_superuser or app_user.rol == 'ADMIN':
                        return redirect('inicio')
                    else:
                        # bodeguero/vendedor/caja solo ven productos
                        return redirect('lista_productos')
                except AppUsuario.DoesNotExist:
                    # Si no existe registro en app, mandar a productos por defecto
                    return redirect('lista_productos')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")

        elif action == 'registro':
            # Public registration is not allowed: only ADMIN/SUPERUSER create users
            if not request.user.is_authenticated:
                messages.error(request, 'Registro deshabilitado. Contacte a un administrador.')
            else:
                # check admin role in app
                try:
                    app_user = AppUsuario.objects.get(username=request.user.username)
                    if not (request.user.is_superuser or app_user.rol == 'ADMIN'):
                        messages.error(request, 'Registro deshabilitado. Solo ADMIN puede crear usuarios.')
                    else:
                        messages.error(request, 'Use el panel de administración para crear usuarios.')
                except AppUsuario.DoesNotExist:
                    messages.error(request, 'Registro deshabilitado. Contacte a un administrador.')

    return render(request, 'login/login.html')


def forgot_password_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        # Try to find user by email or username
        try:
            user = User.objects.filter(email__iexact=identifier).first() or User.objects.filter(username__iexact=identifier).first()
        except Exception:
            user = None

        # If user found, generate token and send email (for testing send to developer email)
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_path = reverse('password_reset_confirm', args=[uid, token])
            reset_link = request.build_absolute_uri(reset_path)
            subject = 'Recuperación de contraseña - ERP Lili\'s'
            message = (
                f"Se ha solicitado restablecer la contraseña para el usuario: {user.username}\n\n"
                f"Use este enlace para definir una nueva contraseña:\n{reset_link}\n\n"
                "Si usted no solicitó este cambio, ignore este correo."
            )
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
            # Send reset link to the user's registered email address when available.
            if user.email:
                try:
                    send_mail(subject, message, from_email, [user.email], fail_silently=getattr(settings, 'EMAIL_FAIL_SILENTLY', True))
                except smtplib.SMTPException as e:
                    logger = logging.getLogger(__name__)
                    logger.exception("Error enviando correo de recuperación de contraseña: %s", e)
                    if not getattr(settings, 'EMAIL_FAIL_SILENTLY', True):
                        messages.warning(request, 'Se generó el token de recuperación, pero no se pudo enviar el correo (problema SMTP).')

        # Always respond with success message to avoid account enumeration
        messages.success(request, 'Si existe una cuenta asociada, se ha enviado un correo con instrucciones.')
        return redirect('login_registro')
    else:
        # GET -> show the forgot password form
        return render(request, 'login/forgot_password.html')


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, 'Enlace inválido o expirado.')
        return redirect('login_registro')

    if request.method == 'POST':
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        if not p1 or not p2:
            messages.error(request, 'Ambas contraseñas son obligatorias.')
        elif p1 != p2:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            ok, msg = validate_password_policy(p1)
            if not ok:
                messages.error(request, msg)
            else:
                user.set_password(p1)
                user.save()
                # update app user if exists
                try:
                    app_user = AppUsuario.objects.get(username=user.username)
                    app_user.password = make_password(p1)
                    app_user.must_change_password = False
                    app_user.save()
                except AppUsuario.DoesNotExist:
                    pass

                messages.success(request, 'Contraseña actualizada. Ahora puede iniciar sesión.')
                return redirect('login_registro')

    return render(request, 'login/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})