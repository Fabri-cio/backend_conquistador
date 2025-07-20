from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

from .models import FacturaVenta, DetalleVenta, Venta
from almacenes.models import Movimiento, TipoMovimiento, Inventario

TIPO_MOVIMIENTO_VENTA = 'Venta'

def generar_pdf_desde_html(template_src, context_dict):
    html = render_to_string(template_src, context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None


@receiver(post_save, sender=DetalleVenta)
@receiver(post_delete, sender=DetalleVenta)
def actualizar_total_venta(sender, instance, **kwargs):
    """
    Actualiza el total de la venta cada vez que se crea, actualiza o elimina un detalle de venta.
    Resta el descuento global de la venta y guarda el total ajustado.
    """
    venta = instance.id_venta
    total = sum(detalle.subtotal for detalle in venta.detalles.all())
    total = max(total - venta.descuento, 0)
    Venta.objects.filter(pk=venta.pk).update(total_venta=total)


@receiver(post_save, sender=DetalleVenta)
def registrar_movimiento(sender, instance, **kwargs):
    """
    Registra un movimiento de venta cuando se crea un detalle de venta.
    """
    try:
        with transaction.atomic():
            venta = instance.id_venta
            inventario = Inventario.objects.select_for_update().get(pk=instance.id_inventario.pk)
            cantidad_vendida = instance.cantidad

            tipo_movimiento = TipoMovimiento.objects.get(nombre=TIPO_MOVIMIENTO_VENTA)

            if inventario.cantidad < cantidad_vendida:
                logger.error(f"Stock insuficiente para {inventario.id_producto.nombre}. Movimiento no registrado.")
                return

            Movimiento.objects.create(
                id_inventario=inventario,
                id_tipo=tipo_movimiento,
                cantidad=cantidad_vendida,
                id_usuario=venta.id_usuario,
            )
    except Exception as e:
        logger.error(f"Error en registrar_movimiento signal: {e}")


@receiver(post_delete, sender=DetalleVenta)
def eliminar_movimiento(sender, instance, **kwargs):
    try:
        Movimiento.objects.filter(
            id_inventario=instance.id_inventario,
            id_usuario=instance.id_venta.id_usuario,
            cantidad=instance.cantidad
        ).delete()
    except Exception as e:
        logger.error(f"Error al eliminar Movimiento relacionado a DetalleVenta: {e}")


@receiver(post_save, sender=Venta)
def crear_factura_automaticamente(sender, instance, created, **kwargs):
    """
    Crea una factura automáticamente cuando se crea una venta.
    Genera un número de factura y registra la factura con el monto total de la venta.
    """
    if created:
        if not hasattr(instance, 'factura'):
            numero_factura = f"F-{instance.id_venta:06d}"
            FacturaVenta.objects.create(
                id_venta=instance,
                numero_factura=numero_factura,
                metodo_pago=instance.metodo_pago,
                monto_total=instance.total_venta
            )


@receiver(post_save, sender=FacturaVenta)
def enviar_factura_condicional(sender, instance, created, **kwargs):
    """
    Envía una factura por correo electrónico cuando se crea una factura.
    Verifica que el cliente tenga correo y que el cliente quiera un comprobante.
    """
    if created:
        venta = instance.id_venta
        cliente = venta.id_cliente

        if cliente and cliente.correo and venta.quiere_comprobante:
            asunto = f"Factura {instance.numero_factura}"
            cuerpo = render_to_string('factura_venta.html', {'factura': instance, 'venta': venta})

            pdf_content = generar_pdf_desde_html('factura_venta.html', {'factura': instance, 'venta': venta})

            email = EmailMessage(
                asunto,
                cuerpo,
                'ventas@tusistema.com',  # Cambia por tu email remitente
                [cliente.correo],
            )
            email.content_subtype = "html"
            if pdf_content:
                email.attach(f"Factura_{instance.numero_factura}.pdf", pdf_content, "application/pdf")
            
            try:
                email.send(fail_silently=False)
            except Exception as e:
                logger.error(f"Error enviando factura por email: {e}")
