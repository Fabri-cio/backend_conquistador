from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import Venta, DetalleVenta
from .services import VentaService

# 1️⃣ Actualizar total de la venta cada vez que se cree/elimine un detalle
@receiver(post_save, sender=DetalleVenta)
@receiver(post_delete, sender=DetalleVenta)
def actualizar_total_signal(sender, instance, **kwargs):
    VentaService.actualizar_total(instance.venta)

# 2️⃣ Registrar movimiento en inventario al crear un detalle
@receiver(post_save, sender=DetalleVenta)
def registrar_movimiento_signal(sender, instance, created, **kwargs):
    if created:
        VentaService.registrar_movimiento(instance)

# 3️⃣ Revertir movimiento al eliminar un detalle
@receiver(post_delete, sender=DetalleVenta)
def eliminar_movimiento_signal(sender, instance, **kwargs):
    VentaService.eliminar_movimiento(instance)

# 4️⃣ Crear comprobante y enviar PDF **después de que la transacción termine**
@receiver(post_save, sender=Venta)
def crear_comprobante_signal(sender, instance, created, **kwargs):
    if created:
        # transaction.on_commit garantiza que todos los detalles estén guardados
        transaction.on_commit(lambda: _crear_y_enviar_pdf(instance))

def _crear_y_enviar_pdf(venta: Venta):
    """
    Crea el comprobante si no existe y envía el PDF.
    """
    comprobante = VentaService.crear_comprobante(venta)
    if comprobante:
        VentaService.enviar_comprobante_async(comprobante)
