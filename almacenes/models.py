from django.db import models
from usuarios.models import CustomUser as User
from productos.models import Producto
from django.core.exceptions import ValidationError


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError

# Almacenes y Tiendas
class Almacen(models.Model):
    id_almacen_tienda = models.AutoField(primary_key=True)  # PK
    nombre = models.CharField(max_length=255, unique=True)  # Nombre del almacén o tienda

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
class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)  # PK
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # FK a Producto
    id_almacen_tienda = models.ForeignKey(Almacen, on_delete=models.CASCADE)  # FK a Almacén
    cantidad = models.PositiveIntegerField(default=0)  # Cantidad de stock disponible
    stock_minimo = models.PositiveIntegerField(default=0)  # Stock mínimo
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    fecha_modificacion = models.DateTimeField(auto_now=True)  # Fecha de última modificación
    usuario_creacion = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='inventario_creado'
    )  # FK a Usuario que creó el registro
    usuario_modificacion = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='inventario_modificado'
    )  # FK a Usuario que modificó el registro
    comentario_modificacion = models.TextField(blank=True, null=True)  # Comentarios opcionales

    def __str__(self):
        return f"{self.id_producto.nombre} - {self.id_almacen_tienda.nombre}"


# Movimientos
class Movimiento(models.Model):
    id_movimiento = models.AutoField(primary_key=True)  # PK
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # FK a Producto
    id_almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='movimientos',null=True, blank=True)  # FK a Almacén
    id_tipo = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)  # FK al Tipo de Movimiento
    cantidad = models.IntegerField()  # Cantidad (positiva para entrada, negativa para salida)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)  # FK a Usuario
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del registro

    def __str__(self):
        return f"{self.cantidad} {self.id_producto.nombre}"

# Señal para actualizar el inventario al guardar un movimiento
@receiver(post_save, sender=Movimiento)
def actualizar_inventario_guardar(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            inventario = Inventario.objects.get(
                id_producto=instance.id_producto,
                id_almacen_tienda=instance.id_almacen
            )

            # Procesar según la naturaleza del movimiento
            if instance.id_tipo.naturelaza == 'Entrada':
                # Sumar al inventario
                inventario.cantidad += abs(instance.cantidad)
            elif instance.id_tipo.naturelaza == 'Salida':
                # Restar del inventario y validar cantidad suficiente
                if abs(instance.cantidad) > inventario.cantidad:
                    raise ValidationError(
                        f"Stock insuficiente para {instance.id_producto.nombre} en el almacén {instance.id_almacen.nombre}."
                    )
                inventario.cantidad -= abs(instance.cantidad)

            # Validar que el inventario nunca sea negativo
            if inventario.cantidad < 0:
                raise ValidationError("El inventario no puede ser negativo.")

            inventario.save()

    except Inventario.DoesNotExist:
        raise ValidationError(
            "No existe inventario para este producto en el almacén especificado."
        )

# Señal para revertir el inventario al eliminar un movimiento
@receiver(post_delete, sender=Movimiento)
def revertir_inventario_eliminar(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            inventario = Inventario.objects.get(
                id_producto=instance.id_producto,
                id_almacen_tienda=instance.id_almacen
            )

            # Revertir la operación según la naturaleza del movimiento
            if instance.id_tipo.naturelaza == 'Entrada':
                # Restar del inventario al revertir una entrada
                inventario.cantidad -= abs(instance.cantidad)
            elif instance.id_tipo.naturelaza == 'Salida':
                # Sumar al inventario al revertir una salida
                inventario.cantidad += abs(instance.cantidad)

            # Validar que el inventario nunca sea negativo
            if inventario.cantidad < 0:
                raise ValidationError("El inventario no puede ser negativo.")

            inventario.save()

    except Inventario.DoesNotExist:
        raise ValidationError(
            "No existe inventario para este producto en el almacén especificado."
        )
