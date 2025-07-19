from django.db.models.signals import post_save
from django.dispatch import receiver
from compras.models import RecepcionPedido, Compra

@receiver(post_save, sender=RecepcionPedido)
def crear_compra_automatica(sender, instance, created, **kwargs):
    if created:
        # Solo crea la compra si no existe ya una asociada
        if not hasattr(instance, 'compra'):
            Compra.objects.create(
                recepcion=instance,
                usuario=instance.usuario,
                observaciones=instance.observaciones
            )
