# services.py
from django.db import transaction
from .models import Venta, DetalleVenta, ComprobanteVenta
from inventarios.models import Movimiento, TipoMovimiento, Inventario
import threading, logging
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.db.models import Sum, F

logger = logging.getLogger(__name__)
TIPO_MOVIMIENTO_VENTA = 'Venta'

class VentaService:

    @staticmethod
    @transaction.atomic
    def registrar_movimiento(detalle: DetalleVenta):
        inventario = Inventario.objects.select_for_update().get(pk=detalle.inventario.pk)
        if inventario.cantidad < detalle.cantidad:
            raise ValueError(f"Stock insuficiente para {inventario.producto.nombre}")
        tipo_movimiento = TipoMovimiento.objects.get(nombre=TIPO_MOVIMIENTO_VENTA)
        Movimiento.objects.create(
            inventario=inventario,
            tipo=tipo_movimiento,
            cantidad=detalle.cantidad,
            usuario_creacion=detalle.venta.usuario_creacion,
        )
        inventario.cantidad -= detalle.cantidad
        inventario.save(update_fields=["cantidad"])

    @staticmethod
    @transaction.atomic
    def eliminar_movimiento(detalle: DetalleVenta):
        Movimiento.objects.filter(
            inventario=detalle.inventario,
            usuario_creacion=detalle.venta.usuario_creacion,
            cantidad=detalle.cantidad
        ).delete()
        detalle.inventario.cantidad += detalle.cantidad
        detalle.inventario.save(update_fields=["cantidad"])

    @staticmethod
    def actualizar_total(venta: Venta):
        total_detalles = venta.detalles.aggregate(total=Sum(F("sub_total")))["total"] or 0
        venta.total_venta = max(0, total_detalles - venta.descuento)
        venta.save(update_fields=["total_venta"])

    @staticmethod
    def crear_comprobante(venta: Venta):
        if venta.quiere_comprobante and not hasattr(venta, "detalle_comprobante"):
            numero = f"F-{venta.id:06d}"
            return ComprobanteVenta.objects.create(venta=venta, numero_comprobante=numero)
        return None

    @staticmethod
    def enviar_comprobante_async(comprobante: ComprobanteVenta):
        """
        Genera el PDF de la factura y lo envía por correo al cliente de forma asíncrona.
        """

        def enviar():
            venta = comprobante.venta
            cliente = venta.cliente

            # Validar que exista cliente y correo
            if not (cliente and cliente.correo):
                logger.warning(f"No se puede enviar factura {comprobante.numero_comprobante}: cliente o correo no disponible")
                return

            # Renderizar plantilla con datos correctos
            contexto = {
                "factura": comprobante,
                "venta": venta,
                "detalles": venta.detalles.all(),
            }
            html = render_to_string("factura_venta.html", contexto)

            # Generar PDF en memoria
            pdf_file = BytesIO()
            pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf_file)
            if pisa_status.err:
                logger.error(f"Error generando PDF de factura {comprobante.numero_comprobante}")
                return

            # Preparar y enviar correo
            asunto = f"Factura {comprobante.numero_comprobante}"
            email = EmailMessage(
                subject=asunto,
                body="Adjuntamos su factura en PDF.",
                from_email="ventas@tusistema.com",
                to=[cliente.correo]
            )
            email.content_subtype = "html"
            email.attach(f"Factura_{comprobante.numero_comprobante}.pdf", pdf_file.getvalue(), "application/pdf")

            try:
                email.send(fail_silently=False)
                logger.info(f"Factura {comprobante.numero_comprobante} enviada a {cliente.correo}")
            except Exception as e:
                logger.error(f"Error enviando factura {comprobante.numero_comprobante}: {e}")

        # Ejecutar en un hilo para no bloquear la petición
        threading.Thread(target=enviar, daemon=True).start()