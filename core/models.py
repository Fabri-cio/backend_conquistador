# core/models.py
from django.db import models
from django.utils import timezone

class AuditoriaBase(models.Model):
    usuario_creacion = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_creados"
    )
    usuario_modificacion = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_modificados"
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    # fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    comentario_modificacion = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
