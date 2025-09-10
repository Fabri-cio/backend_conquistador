from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import DetalleCompra
from .services import CompraService

# 1️⃣ Actualizar total al crear/eliminar detalle
@receiver(post_save, sender=DetalleCompra)
@receiver(post_delete, sender=DetalleCompra)
def actualizar_total_signal(sender, instance, **kwargs):
    CompraService.actualizar_total(instance.compra)

# 2️⃣ Registrar movimiento al crear detalle
@receiver(post_save, sender=DetalleCompra)
def registrar_movimiento_signal(sender, instance, created, **kwargs):
    if created:
        CompraService.registrar_movimiento(instance)

# 3️⃣ Revertir movimiento al eliminar detalle
@receiver(post_delete, sender=DetalleCompra)
def eliminar_movimiento_signal(sender, instance, **kwargs):
    CompraService.eliminar_movimiento(instance)
