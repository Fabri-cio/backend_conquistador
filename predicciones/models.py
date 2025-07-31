from django.db import models
from django.core.exceptions import ValidationError
from core.models import AuditoriaBase

# 🔥 Configuracion de Prophet
class ConfiguracionModelo(models.Model):
    nombre_config = models.CharField(max_length=100)
    modo_crecimiento = models.CharField(max_length=10, choices=[("linear", "Linear"), ("logistic", "Logistic")])
    capacidad_maxima = models.FloatField(null=True, blank=True)
    intervalo_confianza = models.FloatField(default=0.80)

    usar_est_anual = models.BooleanField(default=True)
    fourier_anual = models.IntegerField(default=10)
    usar_est_semanal = models.BooleanField(default=True)
    fourier_semanal = models.IntegerField(default=3)
    usar_est_diaria = models.BooleanField(default=False)
    fourier_diaria = models.IntegerField(null=True, blank=True)

    estacionalidad_modo = models.CharField(max_length=15, choices=[("additive", "Aditiva"), ("multiplicative", "Multiplicativa")], default="additive")

    usar_feriados = models.BooleanField(default=False)
    eventos_especiales = models.JSONField(default=list)
    estacionalidades_personalizadas = models.JSONField(default=list)
    regresores_adicionales = models.JSONField(default=list)

    def __str__(self):
        return f"Configuracion {self.nombre_config}"

class Prediccion(AuditoriaBase):
    inventario = models.ForeignKey('almacenes.Inventario', on_delete=models.CASCADE)  # FK a Inventario
    fecha_prediccion = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la predicción
    configuracion = models.ForeignKey(ConfiguracionModelo, on_delete=models.CASCADE)  # FK a ConfiguracionModelo
    
    # 🔥 NUEVO: Rango de fechas de la predicción generada
    fecha_inicio_predicha = models.DateField()
    fecha_fin_predicha = models.DateField()

    # 🔥 NUEVO: Cantidad predicha
    resultado_prediccion = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Prediccion {self.fecha_prediccion}"

    def clean(self):
        if self.fecha_inicio_predicha > self.fecha_fin_predicha:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

class DetallePrediccion(models.Model):
    cantidad = models.IntegerField()  # Cantidad predicha
    fecha_predicha = models.DateField()
    id_prediccion = models.ForeignKey(Prediccion, on_delete=models.CASCADE, related_name='detalles')  # FK a Prediccion

    # 🔥 NUEVO: A qué fecha corresponde la predicción de esta cantidad

    def __str__(self):
        return f"Detalle Prediccion {self.fecha_predicha}"


