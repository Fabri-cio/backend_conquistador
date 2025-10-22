# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from inventarios.models import Inventario, Notificacion

@receiver(post_save, sender=Inventario)
def notificar_stock_bajo(sender, instance, **kwargs):
    # Solo si el stock está bajo
    if instance.cantidad > instance.stock_minimo:
        return

    # Evitar duplicados: ya existe notificación para este inventario y tipo 'warning'
    if Notificacion.objects.filter(inventario=instance, tipo='warning').exists():
        return

    # Crear notificación
    notificacion = Notificacion.objects.create(
        titulo=f"Stock bajo: {instance.producto.nombre}",
        mensaje=f"El producto {instance.producto.nombre} tiene solo {instance.cantidad} unidades.",
        tipo="warning",
        inventario=instance
    )

    # Enviar por WebSocket (opcional)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notificaciones_general",  # grupo global de inventario
        {
            "type": "send_notification",
            "data": {
                "id": notificacion.id,
                "titulo": notificacion.titulo,
                "mensaje": notificacion.mensaje,
                "tipo": notificacion.tipo,
                "producto": instance.producto.nombre,
                "almacen": instance.almacen.nombre,
                "cantidad": float(instance.cantidad),
            }
        }
    )
