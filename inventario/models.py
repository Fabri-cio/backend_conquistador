from django.db import models

from productos.models import Producto

# Modelo de Inventario
class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField()
    ubicacion_almacen = models.CharField(max_length=100)

    def __str__(self):
        return f'Inventario de {self.producto.nombre}'
