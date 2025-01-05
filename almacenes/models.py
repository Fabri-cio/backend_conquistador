from django.db import models
from usuarios.models import CustomUser as User
from productos.models import Producto
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

    def __str__(self):
        return self.nombre


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
    id_origen = models.ForeignKey(
        Almacen, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_salida'
    )  # FK al Almacén de origen (puede ser nulo)
    id_destino = models.ForeignKey(
        Almacen, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_entrada'
    )  # FK al Almacén de destino (puede ser nulo)
    id_tipo = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)  # FK al Tipo de Movimiento
    cantidad = models.IntegerField()  # Cantidad (positiva para entrada, negativa para salida)
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha y hora del movimiento
    id_usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # FK a Usuario
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del registro

    def clean(self):
        # Asegura que haya al menos un origen o destino
        if not self.id_origen and not self.id_destino:
            raise ValidationError("Debe especificar al menos un origen o un destino.")
        # Validación lógica para la cantidad
        if self.cantidad == 0:
            raise ValidationError("La cantidad no puede ser cero.")
        # Verificación adicional para traslados
        if self.id_origen == self.id_destino and self.id_origen:
            raise ValidationError("El origen y destino no pueden ser el mismo.")

    def save(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  # Captura el usuario que realiza la operación
        if not self.pk:  # Si es un nuevo registro
            self.id_usuario = usuario
        else:  # Si es una actualización
            self.id_usuario = usuario
        self.clean()  # Llama a las validaciones personalizadas
        super().save(*args, **kwargs)

    def __str__(self):
        movimiento_tipo = f"{self.id_tipo.nombre} ({'Entrada' if self.cantidad > 0 else 'Salida'})"
        return f"{movimiento_tipo}: {self.cantidad} {self.id_producto.nombre} ({self.fecha})"

    class Meta:
        ordering = ['-fecha_creacion']  # Ordena por fecha de creación (más reciente primero)
