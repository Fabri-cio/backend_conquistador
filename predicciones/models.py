from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import AuditoriaBase

# 🔥 Configuración de Prophet (solo almacenamiento)
class ConfiguracionModelo(models.Model):
    """
    Modelo para guardar configuraciones de Prophet sin crear ni entrenar modelos.
    Los valores automáticos se gestionan desde el frontend.
    """
    nombre_config = models.CharField(max_length=100)

    tipo_dataset = models.CharField(
        max_length=20,
        choices=[
            ("normal", "Normal"),
            ("pocos_datos", "Pocos Datos"),
            ("muchos_datos", "Muchos Datos"),
            ("datos_ruidosos", "Datos Ruidosos"),
            ("datos_huecos", "Datos con Huecos"),
        ],
        default="normal"
    )

    modo_crecimiento = models.CharField(
        max_length=10, 
        choices=[("linear", "Linear"), ("logistic", "Logistic")],
        default="linear"
    )
    capacidad_maxima = models.FloatField(null=True, blank=True)
    capacidad_minima = models.FloatField(null=True, blank=True)

    intervalo_confianza = models.FloatField(default=0.80)

    usar_est_anual = models.BooleanField(default=True)
    fourier_anual = models.IntegerField(default=10)
    usar_est_semanal = models.BooleanField(default=True)
    fourier_semanal = models.IntegerField(default=3)
    usar_est_diaria = models.BooleanField(default=False)
    fourier_diaria = models.IntegerField(null=True, blank=True)

    estacionalidad_modo = models.CharField(
        max_length=15,
        choices=[("additive", "Aditiva"), ("multiplicative", "Multiplicativa")],
        default="additive"
    )

    seasonality_prior_scale = models.FloatField(default=10.0)
    holidays_prior_scale = models.FloatField(default=10.0)
    changepoint_prior_scale = models.FloatField(default=0.05)
    n_changepoints = models.IntegerField(default=25)
    changepoints = models.JSONField(default=list)

    usar_feriados = models.BooleanField(default=False)
    eventos_especiales = models.JSONField(default=list)
    estacionalidades_personalizadas = models.JSONField(default=list)
    regresores_adicionales = models.JSONField(default=list)

    incluir_incertidumbre_tendencia = models.BooleanField(default=True)
    incluir_incertidumbre_estacionalidad = models.BooleanField(default=True)

    frecuencia_datos = models.CharField(
        max_length=10,
        choices=[("D", "Diaria"), ("W", "Semanal"), ("M", "Mensual")],
        default="D"
    )

    descripcion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    def clean(self):
        # Intervalo de confianza entre 0 y 1
        if not (0 < self.intervalo_confianza <= 1):
            raise ValidationError("El intervalo de confianza debe estar entre 0 y 1.")

        # Crecimiento logístico requiere capacidad máxima
        if self.modo_crecimiento == "logistic" and self.capacidad_maxima is None:
            raise ValidationError("Para crecimiento logístico, se debe definir capacidad máxima.")

        # Fourier positivo si se usan
        if self.usar_est_anual and (self.fourier_anual is None or self.fourier_anual <= 0):
            raise ValidationError("Fourier anual debe ser positivo si se usa.")
        if self.usar_est_semanal and (self.fourier_semanal is None or self.fourier_semanal <= 0):
            raise ValidationError("Fourier semanal debe ser positivo si se usa.")
        if self.usar_est_diaria and (self.fourier_diaria is None or self.fourier_diaria <= 0):
            raise ValidationError("Fourier diaria debe ser positivo si se usa.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Configuración {self.nombre_config}"

# 🔹 Modelos relacionados con predicciones

class Prediccion(AuditoriaBase):
    inventario = models.ForeignKey('inventarios.Inventario', on_delete=models.CASCADE)
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
    configuracion = models.ForeignKey(ConfiguracionModelo, on_delete=models.CASCADE)

    fecha_inicio_predicha = models.DateField()
    fecha_fin_predicha = models.DateField()
    resultado_prediccion = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        hoy = timezone.now().date()

        if self.fecha_inicio_predicha > self.fecha_fin_predicha:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        if self.fecha_inicio_predicha < hoy or self.fecha_fin_predicha < hoy:
            raise ValidationError("Las fechas de predicción no pueden ser anteriores a hoy.")

        if self.resultado_prediccion < 0:
            raise ValidationError("El resultado de la predicción no puede ser negativo.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prediccion {self.fecha_prediccion} - {self.inventario} - {self.configuracion.nombre_config}"


class DetallePrediccion(models.Model):
    prediccion = models.ForeignKey(Prediccion, on_delete=models.CASCADE, related_name='detalles')
    cantidad = models.IntegerField()
    fecha_predicha = models.DateField()

    def clean(self):
        if self.cantidad < 0:
            raise ValidationError("La cantidad predicha no puede ser negativa.")

        if not (self.prediccion.fecha_inicio_predicha <= self.fecha_predicha <= self.prediccion.fecha_fin_predicha):
            raise ValidationError("La fecha del detalle debe estar dentro del rango de la predicción.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle Prediccion {self.fecha_predicha}"
