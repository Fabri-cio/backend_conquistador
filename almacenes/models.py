from django.db import models
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError
from core.models import AuditoriaBase

# Almacenes y Tiendas
class Almacen(AuditoriaBase):
    id_almacen_tienda = models.AutoField(primary_key=True)  # PK
    nombre = models.CharField(max_length=255, unique=True)  # Nombre del almacén o tienda
    direccion = models.CharField(max_length=255)  # Dirección del almacén o tienda
    telefono = models.CharField(max_length=255)  # Teléfono del almacén o tienda
    es_principal = models.BooleanField(default=False)  # Indica si es el almacén principal
    estado = models.BooleanField(default=True)  # Indica si el almacén está activo

    def __str__(self):
        return self.nombre


# Tipo de Movimiento
class TipoMovimiento(models.Model):
    id_tipo = models.AutoField(primary_key=True)  # PK
    nombre = models.CharField(max_length=255, unique=True)  # Nombre del tipo de movimiento
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional
    naturelaza = models.CharField(
        max_length=10, 
        choices=(('Entrada', 'Entrada'), ('Salida', 'Salida')),
        default='Entrada'
    )

    def __str__(self):
        return f"{self.nombre} ({self.naturelaza})"  


# Inventario
class Inventario(AuditoriaBase):
    id_inventario = models.AutoField(primary_key=True)  # PK
    id_producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)  # FK a Producto
    id_almacen_tienda = models.ForeignKey(Almacen, on_delete=models.CASCADE)  # FK a Almacén
    cantidad = models.PositiveIntegerField(default=0)  # Cantidad de stock disponible
    stock_minimo = models.PositiveIntegerField(default=0)  # Stock mínimo
    stock_maximo = models.PositiveIntegerField(default=0)  # Stock máximo

    def __str__(self):
        return f"{self.id_producto.nombre} - {self.id_almacen_tienda.nombre}"


# Movimientos
class Movimiento(AuditoriaBase):
    id_movimiento = models.AutoField(primary_key=True)  # PK
    id_inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)  # FK a Inventario
    id_tipo = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)  # FK al Tipo de Movimiento
    cantidad = models.IntegerField(help_text="Cantidad del movimiento. Siempre positiva. La naturaleza define si es entrada o salida.")  # Cantidad (positiva para entrada, negativa para salida)

    def __str__(self):
        return f"{self.id_tipo.nombre}: {self.cantidad} x {self.id_inventario.id_producto.nombre} en {self.id_inventario.id_almacen_tienda.nombre}"


# Señal para actualizar el inventario al guardar un movimiento
@receiver(post_save, sender=Movimiento)
def actualizar_inventario_guardar(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            inventario = instance.id_inventario  # YA NO HACE FALTA HACER UN GET

            if instance.id_tipo.naturelaza == 'Entrada':
                inventario.cantidad += abs(instance.cantidad)
            elif instance.id_tipo.naturelaza == 'Salida':
                if abs(instance.cantidad) > inventario.cantidad:
                    raise ValidationError(
                        f"Stock insuficiente para {inventario.id_producto.nombre} en el almacén {inventario.id_almacen_tienda.nombre}."
                    )
                inventario.cantidad -= abs(instance.cantidad)
            if inventario.cantidad < 0:
                raise ValidationError("El inventario no puede ser negativo.")
            inventario.save()
    except Exception as e:
        raise ValidationError(str(e))


# Señal para revertir el inventario al eliminar un movimiento
@receiver(post_delete, sender=Movimiento)
def revertir_inventario_eliminar(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            inventario = instance.id_inventario

            if instance.id_tipo.naturelaza == 'Entrada':
                inventario.cantidad -= abs(instance.cantidad)
            elif instance.id_tipo.naturelaza == 'Salida':
                inventario.cantidad += abs(instance.cantidad)
            if inventario.cantidad < 0:
                raise ValidationError("El inventario no puede ser negativo.")
            inventario.save()
    except Exception as e:
        raise ValidationError(str(e))

