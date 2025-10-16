# core/management/commands/importar_ventas_json.py
from decimal import Decimal
import json
from django.core.management.base import BaseCommand
from django.db import transaction
from ventas.models import Venta, DetalleVenta
from inventarios.models import Inventario
from django.contrib.auth import get_user_model
from ventas.services import VentaService
from django.utils.dateparse import parse_datetime
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = "Importa ventas masivas desde JSON de manera más rápida y mostrando progreso."

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

        ventas_creadas = 0
        detalles_creados = 0

        total_ventas = len(ventas_data)
        self.stdout.write(f"Procesando {total_ventas} ventas...")

        for idx, venta_item in enumerate(ventas_data, start=1):
            # Fecha personalizada
            fecha_str = venta_item.get("fecha_creacion")
            fecha = parse_datetime(fecha_str) if fecha_str else timezone.now()
            if fecha_str and not fecha:
                self.stdout.write(self.style.WARNING(f"Fecha inválida '{fecha_str}', se usará fecha actual."))
                fecha = timezone.now()

            with transaction.atomic():
                venta = Venta.objects.create(
                    tienda_id=venta_item["tienda_id"],
                    usuario_creacion=usuario,
                    descuento=Decimal(str(venta_item.get("descuento", 0))),
                    metodo_pago=venta_item.get("metodo_pago", "Efectivo"),
                    quiere_comprobante=False,
                    fecha_creacion=fecha
                )
                ventas_creadas += 1

                detalles_objs = []
                for producto in venta_item.get("productos", []):
                    try:
                        inventario = Inventario.objects.select_for_update().get(pk=producto["inventario_id"])
                    except Inventario.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Inventario {producto['inventario_id']} no existe."))
                        continue

                    cantidad = Decimal(str(producto["cantidad"]))
                    precio_unitario = Decimal(str(producto["precio_unitario"]))
                    descuento_unitario = Decimal(str(producto.get("descuento_unitario", 0)))

                    if inventario.cantidad < cantidad:
                        self.stdout.write(self.style.WARNING(
                            f"Stock insuficiente para {inventario.producto.nombre}. Disponible: {inventario.cantidad}, requerido: {cantidad}"
                        ))
                        continue

                    detalles_objs.append(
                        DetalleVenta(
                            venta=venta,
                            inventario=inventario,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento_unitario=descuento_unitario,
                            sub_total=(cantidad * precio_unitario) - descuento_unitario
                        )
                    )

                    # Reducir stock
                    inventario.cantidad -= cantidad
                    inventario.save(update_fields=["cantidad"])

                DetalleVenta.objects.bulk_create(detalles_objs)
                detalles_creados += len(detalles_objs)

                # Actualizar total de la venta
                VentaService.actualizar_total(venta)

            if idx % 10 == 0 or idx == total_ventas:
                self.stdout.write(f"Procesadas {idx}/{total_ventas} ventas")

        self.stdout.write(self.style.SUCCESS(
            f"Importación finalizada. Ventas creadas: {ventas_creadas}, Detalles creados: {detalles_creados}"
        ))
