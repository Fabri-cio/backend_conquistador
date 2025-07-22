from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

from .models import DetalleCompra, Compra
from almacenes.models import Inventario, Movimiento, TipoMovimiento

TIPO_MOVIMIENTO_COMPRA = 'Compra'

@receiver(post_save, sender=DetalleCompra)
def actualizar_total_compra(sender, instance, **kwargs):
    """
    Actualiza el total de la compra cada vez que se crea, actualiza o elimina un detalle de compra.
    Resta el descuento global de la compra y guarda el total ajustado.
    """
    compra = instance.id_compra
    total = sum(detalle.subtotal for detalle in compra.detalles.all())
    total = max(total - compra.descuento, 0)
    Compra.objects.filter(pk=compra.pk).update(total_compra=total)

@receiver(post_save, sender=DetalleCompra)
def registrar_movimiento(sender, instance, **kwargs):
    """
    Registra un movimiento de compra cuando se crea un detalle de compra.
    """
    try:
        with transaction.atomic():
            compra = instance.id_compra
            inventario = Inventario.objects.select_for_update().get(pk=instance.id_inventario.pk)
            cantidad_comprada = instance.cantidad

            tipo_movimiento = TipoMovimiento.objects.get(nombre=TIPO_MOVIMIENTO_COMPRA)
            
            Movimiento.objects.create(
                id_inventario=inventario,
                id_tipo=tipo_movimiento,
                cantidad=cantidad_comprada,
                id_usuario=compra.id_usuario,
            )
    except Exception as e:
        logger.error(f"Error en registrar_movimiento signal: {e}")

@receiver(post_delete, sender=DetalleCompra)
def eliminar_movimiento(sender, instance, **kwargs):
    try:
        Movimiento.objects.filter(
            id_inventario=instance.id_inventario,
            id_usuario=instance.id_compra.id_usuario,
            cantidad=instance.cantidad
        ).delete()
    except Exception as e:
        logger.error(f"Error al eliminar Movimiento relacionado a DetalleCompra: {e}")


