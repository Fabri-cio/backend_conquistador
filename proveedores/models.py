from django.db import models

from productos.models import Producto

# Modelo de Proveedor
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField()

    def __str__(self):
        return self.nombre

# Modelo de Orden de Compra
class OrdenCompra(models.Model):
    id_orden = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return f'Orden {self.id_orden} - {self.estado}'

# Modelo de Detalles de la Orden
class DetalleOrden(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} unidades'
