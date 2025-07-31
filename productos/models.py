from django.db import models
from core.models import AuditoriaBase
from simple_history.models import HistoricalRecords

# Modelo de Categoría
class Categoria(AuditoriaBase):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)

    def __str__(self):
        return self.nombre_categoria
    
class Proveedor(AuditoriaBase):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='proveedores/', null=True, blank=True)

    def __str__(self):
        return self.nombre_proveedor

# Modelo de Producto
class Producto(AuditoriaBase):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    # marca = models.CharField(max_length=100)  # Si lo necesitas
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    codigo_barras = models.CharField(max_length=50, unique=True)  # Asegura que el código de barras sea único
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    documento = models.FileField(upload_to='productos/documentos/', null=True, blank=True)
    history = HistoricalRecords() #añade el historial

    def __str__(self):
        return self.nombre

