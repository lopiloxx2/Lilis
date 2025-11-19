from productos.models import Usuario as AppUsuario

def app_user(request):
    """Add the application Usuario (if any) to the template context as `app_user`.
    This lets templates check the app role without extra queries.
    """
    # Always provide the `app_user` key so templates can safely check it.
    if not request.user.is_authenticated:
        return {'app_user': None}
    try:
        u = AppUsuario.objects.get(username=request.user.username)
        return {'app_user': u}
    except AppUsuario.DoesNotExist:
        return {'app_user': None}
