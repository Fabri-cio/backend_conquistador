from django.db import models
from core.models import AuditoriaBase
from simple_history.models import HistoricalRecords

# Modelo de Categoría
class Categoria(AuditoriaBase):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Proveedor(AuditoriaBase):
    marca = models.CharField("Marca",max_length=100,blank=True,null=True,unique=True)
    contacto = models.CharField("Nombre de Contacto",max_length=100,blank=True,null=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='proveedores/', null=True, blank=True)

    def __str__(self):
        return self.marca

# Modelo de Producto
class Producto(AuditoriaBase):
    nombre = models.CharField(max_length=100)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    codigo_barras = models.CharField(max_length=50, unique=True)#unique unico barcode
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    documento = models.FileField(upload_to='productos/documentos/', null=True, blank=True)
    history = HistoricalRecords() #añade el historial

    def __str__(self):
        return self.nombre

