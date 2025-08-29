# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Venta, DetalleVenta
from .services import VentaService

@receiver(post_save, sender=DetalleVenta)
@receiver(post_delete, sender=DetalleVenta)
def actualizar_total_signal(sender, instance, **kwargs):
    VentaService.actualizar_total(instance.venta)

@receiver(post_save, sender=DetalleVenta)
def registrar_movimiento_signal(sender, instance, created, **kwargs):
    if created:
        VentaService.registrar_movimiento(instance)

@receiver(post_delete, sender=DetalleVenta)
def eliminar_movimiento_signal(sender, instance, **kwargs):
    VentaService.eliminar_movimiento(instance)

@receiver(post_save, sender=Venta)
def crear_comprobante_signal(sender, instance, created, **kwargs):
    if created:
        comprobante = VentaService.crear_comprobante(instance)
        if comprobante:
            VentaService.enviar_comprobante_async(comprobante)
