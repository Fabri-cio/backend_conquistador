from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from productos.models import Producto
from usuarios.models import CustomUser as User
from almacenes.models import Almacen
from almacenes.models import Movimiento, TipoMovimiento, Inventario
from django.db import transaction
from django.core.exceptions import ValidationError

# Definir la clase Venta
class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tienda = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50, default="Efectivo",editable=False)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Descuento global de la venta
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta {self.id_venta} - {self.fecha_venta}"

# Definir los detalles de la venta
class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Detalle de Venta {self.id_detalle_venta} - Producto {self.id_producto}"

    # # Método para calcular el subtotal de este detalle
    def save(self, *args, **kwargs):
        if self.precio_unitario is None:
            raise ValidationError("El precio unitario no puede ser nulo.")
        self.subtotal = (self.cantidad * self.precio_unitario) - self.descuento_unitario
        if self.subtotal < 0:
            raise ValidationError("El subtotal no puede ser negativo.")
        super().save(*args, **kwargs)
# # Señales para actualizar el total de la venta
@receiver(post_save, sender=DetalleVenta)
@receiver(post_delete, sender=DetalleVenta)
def actualizar_total_venta(sender, instance, **kwargs):
    venta = instance.id_venta
    total = sum(detalle.subtotal for detalle in venta.detalles.all())
    total -= venta.descuento if total > venta.descuento else total
    venta.total_venta = total
    venta.save()

@receiver(post_save, sender=DetalleVenta)
def registrar_movimiento(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            venta = instance.id_venta
            producto = instance.id_producto
            cantidad_vendida = instance.cantidad
            tienda_origen = venta.id_tienda

            # Verificar si el producto tiene inventario en la tienda
            inventario = Inventario.objects.filter(id_producto=producto, id_almacen_tienda=tienda_origen).first()
            if not inventario:
                raise ValidationError(f"El producto {producto.nombre} no tiene inventario registrado en esta tienda.")
            
            if inventario.cantidad < cantidad_vendida:
                raise ValidationError("No hay suficiente stock para este producto.")

            # Registrar el movimiento
            tipo_movimiento = TipoMovimiento.objects.get(nombre='Venta')
            Movimiento.objects.create(
                id_producto=producto,
                id_almacen=tienda_origen,
                id_tipo=tipo_movimiento,
                cantidad=cantidad_vendida,
                id_usuario=venta.id_usuario,
            )

            # Actualizar el inventario
            inventario.cantidad -= cantidad_vendida
            inventario.save()

    except ValidationError as e:
        # Asegúrate de que la excepción sea propagada correctamente
        raise ValidationError(f"Error al registrar el movimiento: {e}")
    except Exception as e:
        # Cualquier otra excepción también será propagada
        raise ValidationError(f"Error al registrar el movimiento: {e}")