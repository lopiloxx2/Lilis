from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilUsuario, UserProfile

@receiver(post_save, sender=User)
def crear_perfiles(sender, instance, created, **kwargs):
    if created:
        # Crear PerfilUsuario sin datos adicionales aún
        PerfilUsuario.objects.create(
            user=instance,
            rut="11.111.111-1",  # valor temporal si deseas obligatorio
        )
        # Crear perfil para cambio de contraseña
        UserProfile.objects.create(user=instance)
