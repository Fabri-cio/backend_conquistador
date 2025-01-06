from django.db import models
from usuarios.models import CustomUser as User
from productos.models import Producto

class Prediccion(models.Model):
    id_prediccion = models.AutoField(primary_key=True)  # PK
    fecha_prediccion = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la predicción
    usuario_responsable = models.ForeignKey(User, on_delete=models.CASCADE)  # FK a Usuario responsable
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # FK a Producto
    resultado_prediccion = models.DecimalField(max_digits=10, decimal_places=2)  # Resultado de la predicción
    model_used = models.CharField(max_length=255)  # Modelo utilizado para la predicción

    def __str__(self):
        return f"Prediccion {self.producto.nombre} - {self.fecha_prediccion}"
