from django.db import models
from productos.models import Producto

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateField()
    forma_pago = models.CharField(max_length=50, default="Efectivo")
    id_empleado = models.IntegerField()

    def calcular_total(self):
        total = sum(detalle.cantidad * detalle.precio_venta for detalle in self.detalles.all())
        return total
    
    def save(self, *args, **kwargs):
        # Guardar la instancia primero para generar el PK
        super().save(*args, **kwargs)
        
        # Ahora que la venta tiene un PK, podemos calcular el total
        self.total_venta = self.calcular_total()
        
        # Guardamos de nuevo para actualizar el campo total_venta
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Venta {self.id_venta} - {self.fecha_venta}"

class DetalleVenta(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.IntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id_detalle} - Venta {self.venta.id_venta}"
