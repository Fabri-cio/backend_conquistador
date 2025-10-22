from django.db import models
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError
from core.models import AuditoriaBase

# Almacenes y Tiendas
class Almacen(AuditoriaBase):
    nombre = models.CharField(max_length=255, unique=True)  # Nombre del almacén o tienda
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Dirección del almacén o tienda
    telefono = models.CharField(max_length=255, blank=True, null=True)  # Teléfono del almacén o tienda
    es_principal = models.BooleanField(default=False)  # Indica si es el almacén principal
    estado = models.BooleanField(default=True)  # Indica si el almacén está activo

    def __str__(self):
        return self.nombre


# Tipo de Movimiento
class TipoMovimiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)  # Nombre del tipo de movimiento
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional
    naturaleza = models.CharField(
        max_length=10, 
        choices=(('Entrada', 'Entrada'), ('Salida', 'Salida')),
        default='Entrada'
    )

    def __str__(self):
        return f"{self.nombre} ({self.naturaleza})"  


# Inventario
class Inventario(AuditoriaBase):
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)  # FK a Producto
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)  # FK a Almacén
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, default=0, help_text="Cantidad de stock disponible")
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=0, help_text="Stock mínimo")  # Stock mínimo
    stock_maximo = models.DecimalField(max_digits=10, decimal_places=3, default=0, help_text="Stock máximo")  # Stock máximo
    estado = models.BooleanField(default=True)  # Indica si el inventario está activo

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['producto', 'almacen'],
                name='unique_inventario'
            )
        ]

    def __str__(self):
        return f"{self.producto.nombre} - {self.almacen.nombre}"


# Movimientos
class Movimiento(AuditoriaBase):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)  # FK a Inventario
    tipo = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)  # FK al Tipo de Movimiento
    cantidad = models.IntegerField(help_text="Cantidad del movimiento. Siempre positiva. La naturaleza define si es entrada o salida.")  # Cantidad (positiva para entrada, negativa para salida)

    def __str__(self):
        return f"{self.tipo.nombre}: {self.cantidad} x {self.inventario.producto.nombre} en {self.inventario.almacen.nombre}"


# Señal para actualizar el inventario al guardar un movimiento
@receiver(post_save, sender=Movimiento)
def actualizar_inventario_guardar(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            inventario = instance.inventario  # YA NO HACE FALTA HACER UN GET

            if instance.tipo.naturaleza == 'Entrada':
                inventario.cantidad += abs(instance.cantidad)
            elif instance.tipo.naturaleza == 'Salida':
                if abs(instance.cantidad) > inventario.cantidad:
                    raise ValidationError(
                        f"Stock insuficiente para {inventario.producto.nombre} en el almacén {inventario.almacen.nombre}."
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
            inventario = instance.inventario

            if instance.tipo.naturaleza == 'Entrada':
                inventario.cantidad -= abs(instance.cantidad)
            elif instance.tipo.naturaleza == 'Salida':
                inventario.cantidad += abs(instance.cantidad)
            if inventario.cantidad < 0:
                raise ValidationError("El inventario no puede ser negativo.")
            inventario.save()
    except Exception as e:
        raise ValidationError(str(e))

class Notificacion(models.Model):
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('info','Información'),
            ('warning','Advertencia'),
            ('error','Error')
        ],
        default='info'
    )
    leida = models.BooleanField(default=False)
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.titulo}"

