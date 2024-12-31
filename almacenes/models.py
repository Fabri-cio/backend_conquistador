from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import User
from productos.models import Producto

class AlmacenOTienda(models.Model):
    """Tabla: Almacenes y Tiendas"""
    id_almacen_o_tienda = models.AutoField(primary_key=True)  # Identificador único del almacén o tienda
    nombre = models.CharField(max_length=255)  # Nombre descriptivo del almacén o tienda (Ej: "Tienda 1")

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    """Tabla: Inventario"""
    id_inventario = models.AutoField(primary_key=True)  # Identificador único del registro
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto del que se está registrando el stock
    almacen_o_tienda = models.ForeignKey(AlmacenOTienda, on_delete=models.CASCADE)  # Ubicación del stock
    cantidad = models.IntegerField()  # Cantidad de stock disponible
    stock_minimo = models.IntegerField()  # Nivel de stock mínimo
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del registro
    fecha_modificacion = models.DateTimeField(auto_now=True)  # Fecha de la última modificación
    usuario_creacion = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='inventarios_creados'
    )  # Usuario que creó el registro
    usuario_modificacion = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='inventarios_modificados'
    )  # Usuario que realizó la última modificación
    comentario_modificacion = models.TextField(blank=True, null=True)  # Comentarios adicionales sobre la modificación

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(cantidad__gte=0), name='cantidad_no_negativa'),
            models.CheckConstraint(check=models.Q(stock_minimo__gte=0), name='stock_minimo_no_negativo'),
        ]

    def __str__(self):
        return f"{self.producto.nombre} - {self.almacen_o_tienda.nombre}"


class TipoMovimiento(models.Model):
    """Tabla: Tipo de Movimiento"""
    id_tipo = models.AutoField(primary_key=True)  # Identificador único del tipo de movimiento
    nombre = models.CharField(max_length=100)  # Nombre del tipo de movimiento (Ej: "Compra", "Traslado")
    descripcion = models.TextField(blank=True, null=True)  # Descripción del tipo de movimiento (opcional)

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    """Tabla: Movimientos"""
    id_movimiento = models.AutoField(primary_key=True)  # Identificador único del movimiento
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto afectado
    origen = models.ForeignKey(
        AlmacenOTienda, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='movimientos_salida'
    )  # Ubicación de origen (puede ser nulo)
    destino = models.ForeignKey(
        AlmacenOTienda, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='movimientos_entrada'
    )  # Ubicación de destino (puede ser nulo)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)  # Tipo de movimiento
    cantidad = models.IntegerField()  # Cantidad de productos movidos
    fecha = models.DateTimeField()  # Fecha y hora del movimiento
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que registró el movimiento
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha en que se creó el movimiento

    def clean(self):
        """Validación personalizada para movimientos."""
        if not self.origen and not self.destino:
            raise ValidationError("Debe haber al menos un origen o destino para el movimiento.")

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(cantidad__gte=0), name='movimiento_cantidad_no_negativa'),
        ]

    def __str__(self):
        return f"{self.tipo_movimiento.nombre} - {self.producto.nombre} - {self.cantidad}"
