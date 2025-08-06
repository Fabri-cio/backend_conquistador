from django.db import models
from django.core.exceptions import ValidationError
from core.models import AuditoriaBase


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Definir la clase Venta
class Venta(AuditoriaBase):
    tienda = models.ForeignKey('inventarios.Almacen', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, default="Efectivo")
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Descuento global de la venta
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quiere_comprobante = models.BooleanField(default=False, help_text="Indica si el cliente quiere recibir factura por email")

    def __str__(self):
        return f"Venta {self.id}  {self.fecha_creacion}"

    # --- 2. Validación para que descuento no supere el total ---
    def clean(self):
        super().clean()
        if self.descuento > self.total_venta:
            raise ValidationError("El descuento no puede ser mayor al total de la venta.")

    def save(self, *args, **kwargs):
        self.clean()  # Validamos antes de guardar
        super().save(*args, **kwargs)

class ComprobanteVenta(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='comprobante')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    numero_comprobante = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Comprobante {self.numero_comprobante}"

# Definir los detalles de la venta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    inventario = models.ForeignKey('inventarios.Inventario', on_delete=models.CASCADE, related_name='ventas')  # <-- cambio aquí
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Detalle de Venta {self.id} - Inventario {self.inventario.producto.nombre}"

    # # Método para calcular el subtotal de este detalle
    def save(self, *args, **kwargs):
        if self.precio_unitario is None:
            raise ValidationError("El precio unitario no puede ser nulo.")

        inventario = self.inventario
        if not inventario:
            raise ValidationError("No se ha especificado inventario válido.")
    
        if inventario.cantidad < self.cantidad:
            raise ValidationError(f"No hay suficiente stock para el producto {inventario.producto.nombre}. Disponible: {inventario.cantidad}.")

        self.subtotal = (self.cantidad * self.precio_unitario) - self.descuento_unitario
        if self.subtotal < 0:
            raise ValidationError("El subtotal no puede ser negativo.")

        super().save(*args, **kwargs)
