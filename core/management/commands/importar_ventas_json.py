# core/management/commands/importar_ventas_json.py
from decimal import Decimal
import json
from django.core.management.base import BaseCommand
from ventas.models import Venta, DetalleVenta
from inventarios.models import Inventario
from django.contrib.auth import get_user_model
from ventas.services import VentaService
from django.utils.dateparse import parse_datetime
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = "Importa ventas masivas desde JSON de manera ultra rápida (sin afectar inventario)."

    def add_arguments(self, parser):
        parser.add_argument("archivo_json", type=str, help="Archivo JSON de ventas")
        parser.add_argument("--usuario", type=int, required=True, help="ID del usuario que realiza las ventas")

    def handle(self, *args, **options):
        archivo_json = options["archivo_json"]
        usuario_id = options["usuario"]

        try:
            usuario = User.objects.get(pk=usuario_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Usuario {usuario_id} no existe"))
            return

        with open(archivo_json, encoding='utf-8') as f:
            ventas_data = json.load(f)

        total_ventas = len(ventas_data)
        self.stdout.write(f"Procesando {total_ventas} ventas...")

        # Traer todos los inventarios que se usarán de una vez
        inventario_ids = {p["inventario_id"] for v in ventas_data for p in v.get("productos", [])}
        inventarios = Inventario.objects.filter(pk__in=inventario_ids).select_related('producto')
        inventario_map = {inv.pk: inv for inv in inventarios}

        ventas_objs = []
        detalles_objs = []

        # Crear instancias de venta en memoria
        for idx, venta_item in enumerate(ventas_data):
            fecha_str = venta_item.get("fecha_creacion")
            fecha = parse_datetime(fecha_str) if fecha_str else timezone.now()
            if fecha_str and not fecha:
                fecha = timezone.now()

            venta = Venta(
                tienda_id=venta_item["tienda_id"],
                usuario_creacion=usuario,
                descuento=Decimal(str(venta_item.get("descuento", 0))),
                metodo_pago=venta_item.get("metodo_pago", "Efectivo"),
                quiere_comprobante=False,
                fecha_creacion=fecha
            )
            ventas_objs.append(venta)

        # Guardar todas las ventas de golpe
        Venta.objects.bulk_create(ventas_objs)
        ventas_creadas = len(ventas_objs)

        # Mapear ID de venta a instancia creada
        ventas_creadas_objs = Venta.objects.order_by("-id")[:ventas_creadas]
        venta_map = {i: v for i, v in enumerate(ventas_creadas_objs)}

        # Crear todos los detalles de golpe
        for idx, venta_item in enumerate(ventas_data):
            venta = venta_map[idx]
            for producto in venta_item.get("productos", []):
                inventario = inventario_map.get(producto["inventario_id"])
                if not inventario:
                    continue

                cantidad = Decimal(str(producto["cantidad"]))
                precio_unitario = inventario.producto.precio
                detalles_objs.append(
                    DetalleVenta(
                        venta=venta,
                        inventario=inventario,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        descuento_unitario=Decimal(0),
                        sub_total=cantidad * precio_unitario
                    )
                )

        DetalleVenta.objects.bulk_create(detalles_objs)
        detalles_creados = len(detalles_objs)

        # Actualizar totales de todas las ventas
        for venta in ventas_creadas_objs:
            VentaService.actualizar_total(venta)

        self.stdout.write(self.style.SUCCESS(
            f"Importación ultra rápida finalizada. Ventas creadas: {ventas_creadas}, Detalles creados: {detalles_creados}"
        ))
