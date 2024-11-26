from django.db import models

# Modelo de Categoría
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_categoria

# Modelo de Producto
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)  # Si lo necesitas
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    codigo_barras = models.CharField(max_length=50, unique=True)  # Asegura que el código de barras sea único

    def __str__(self):
        return self.nombre
