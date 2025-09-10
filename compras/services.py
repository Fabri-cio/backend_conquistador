from django.db import transaction
from django.db.models import Sum, F
from .models import Compra, DetalleCompra
from inventarios.models import Inventario, Movimiento, TipoMovimiento
import logging

logger = logging.getLogger(__name__)
TIPO_MOVIMIENTO_COMPRA = 'Compra'


class CompraService:

    @staticmethod
    @transaction.atomic
    def registrar_movimiento(detalle: DetalleCompra):
        inventario = Inventario.objects.select_for_update().get(pk=detalle.inventario.pk)
        tipo_movimiento = TipoMovimiento.objects.get(nombre=TIPO_MOVIMIENTO_COMPRA)

        # Registrar movimiento
        Movimiento.objects.create(
            inventario=inventario,
            tipo=tipo_movimiento,
            cantidad=detalle.cantidad,
            usuario_creacion=detalle.compra.usuario_creacion,
        )

        # Aumentar stock
        inventario.cantidad += detalle.cantidad
        inventario.save(update_fields=["cantidad"])

    @staticmethod
    @transaction.atomic
    def eliminar_movimiento(detalle: DetalleCompra):
        Movimiento.objects.filter(
            inventario=detalle.inventario,
            usuario_creacion=detalle.compra.usuario_creacion,
            cantidad=detalle.cantidad
        ).delete()

        # Revertir stock
        detalle.inventario.cantidad -= detalle.cantidad
        detalle.inventario.save(update_fields=["cantidad"])

    @staticmethod
    def actualizar_total(compra: Compra):
        subtotal = compra.detalles.aggregate(total=Sum(F("subtotal")))["total"] or 0
        compra.subtotal_compra = subtotal
        compra.total_compra = max(0, subtotal - compra.descuento)
        compra.save(update_fields=["subtotal_compra", "total_compra"])
