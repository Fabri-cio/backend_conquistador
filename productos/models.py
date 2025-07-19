from django.db import models
from simple_history.models import HistoricalRecords

# Modelo de Categoría
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)
    usuario_creacion = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.SET_NULL, null=True, related_name='categoria_creada'
    )  # FK a Usuario que creó el registro
    usuario_modificacion = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.SET_NULL, null=True, related_name='categoria_modificada'
    )  # FK a Usuario que modificó el registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_categoria
    
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='proveedores/', null=True, blank=True)
    usuario_creacion = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.SET_NULL, null=True, related_name='proveedor_creado'
    )  # FK a Usuario que creó el registro
    usuario_modificacion = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.SET_NULL, null=True, related_name='proveedor_modificado'
    )  # FK a Usuario que modificó el registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_proveedor

# Modelo de Producto
class Producto(models.Model):
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
    usuario_creacion = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.SET_NULL, null=True, related_name='producto_creado'
    )  # FK a Usuario que creó el registro
    usuario_modificacion = models.ForeignKey(
        'usuarios.Usuario', on_delete=models.SET_NULL, null=True, related_name='producto_modificado'
    )  # FK a Usuario que modificó el registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    history = HistoricalRecords() #añade el historial


    def __str__(self):
        return self.nombre

