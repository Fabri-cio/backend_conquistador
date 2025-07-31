from django.db import models
from django.core.exceptions import ValidationError
from core.models import AuditoriaBase

# Create your models here.
class Pedido(AuditoriaBase):
    id_pedido = models.AutoField(primary_key=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    proveedor = models.ForeignKey('productos.Proveedor', on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id_pedido}"

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad_solicitada = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_solicitada}"

class Compra(AuditoriaBase):
    id_compra = models.AutoField(primary_key=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    id_tienda = models.ForeignKey('almacenes.Almacen', on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0)     

class DetalleCompra(models.Model):
    id_detalle_compra = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="detalles")
    id_inventario = models.ForeignKey('almacenes.Inventario', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)                
    descuento_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de Compra {self.id_detalle_compra} - Inventario {self.id_inventario}"

    def save(self, *args, **kwargs):
        # 1. Si precio_unitario es None, se asigna 0
        if self.precio_unitario is None:
            self.precio_unitario = 0

        # 2. Verificar que el inventario relacionado exista
        inventario = self.id_inventario
        if not inventario:
            raise ValidationError("No se ha especificado inventario válido.")

        # 3. Verificar que la cantidad no supere el stock máximo permitido para la compra
        #    (aquí depende de la lógica de negocio, pero asumimos que la cantidad puede aumentar stock)
        #    Por ejemplo, si quieres limitar que la cantidad recepcionada no supere cierta cantidad:
        #    (Si no hay restricción específica, puedes omitir esta validación)
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")

        # 4. Calcular subtotal: (cantidad * precio_unitario) - descuento_unitario
        self.subtotal = (self.cantidad * self.precio_unitario) - self.descuento_unitario

        # 5. Validar que el subtotal no sea negativo
        if self.subtotal < 0:
            raise ValidationError("El subtotal no puede ser negativo.")

        # Guardar el objeto
        super().save(*args, **kwargs)



