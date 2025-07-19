from django.db import models

# Create your models here.
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey('productos.Proveedor', on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=20, 
        choices=[("pendiente", "Pendiente"), ("recibido", "Recibido")], 
        default="pendiente"
    )
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id_pedido}"

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    pedido = models.ForeignKey('compras.Pedido', on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad_solicitada = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_solicitada}"

class RecepcionPedido(models.Model):
    id_recepcion = models.AutoField(primary_key=True)
    pedido = models.OneToOneField('compras.Pedido', on_delete=models.CASCADE)
    fecha_recepcion = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(blank=True, null=True)

    total_bruto = models.DecimalField(max_digits=12, decimal_places=2, default=0)   
    total_descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_neto = models.DecimalField(max_digits=12, decimal_places=2, default=0)     

    def actualizar_totales(self):
        detalles = self.detalles.all()
        total_bruto = sum(d.cantidad_recibida * d.precio_unitario for d in detalles)
        total_descuento = sum(d.descuento for d in detalles)
        total_neto = total_bruto - total_descuento

        self.total_bruto = total_bruto
        self.total_descuento = total_descuento
        self.total_neto = total_neto
        self.save(update_fields=['total_bruto', 'total_descuento', 'total_neto'])

    def __str__(self):
        return f"Recepción de Pedido #{self.pedido.id_pedido}"

class DetalleRecepcion(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    recepcion = models.ForeignKey('compras.RecepcionPedido', on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad_recibida = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)                
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = (self.cantidad_recibida * self.precio_unitario) - self.descuento
        super().save(*args, **kwargs)
        self.recepcion.actualizar_totales()

    def __str__(self):
        return f"{self.producto.nombre} - Recibido: {self.cantidad_recibida}"

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    recepcion = models.OneToOneField('compras.RecepcionPedido', on_delete=models.CASCADE)
    fecha_compra = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Compra #{self.id_compra}"

