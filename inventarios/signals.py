from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notificacion
from inventarios.models import Inventario
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()

@receiver(post_save, sender=Inventario)
def notificar_stock_bajo(sender, instance, **kwargs):
    if instance.cantidad <= instance.stock_minimo:
        admins = User.objects.filter(is_staff=True)
        channel_layer = get_channel_layer()
        for admin in admins:
            notificacion = Notificacion.objects.create(
                usuario=admin,
                titulo=f"Stock bajo: {instance.producto.nombre}",
                mensaje=f"El producto {instance.producto.nombre} tiene solo {instance.cantidad} unidades.",
                tipo="warning",
                inventario=instance
            )
            async_to_sync(channel_layer.group_send)(
                f"user_{admin.id}",
                {
                    "type": "send_notification",
                    "data": {
                        "titulo": notificacion.titulo,
                        "mensaje": notificacion.mensaje,
                        "tipo": notificacion.tipo,
                        "producto": instance.producto.nombre,
                        "almacen": instance.almacen.nombre,
                        "cantidad": float(instance.cantidad),
                    }
                }
            )
