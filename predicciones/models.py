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
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre identificador de la configuración."
    )

    dataset = models.CharField(
        max_length=20,
        choices=[
            ("normal", "Normal"),
            ("pocos", "Pocos Datos"),
            ("muchos", "Muchos Datos"),
            ("ruidosos", "Datos Ruidosos"),
            ("huecos", "Datos con Huecos"),
        ],
        default="normal",
        help_text="Tipo de dataset con el que trabajará el modelo."
    )

    crecimiento = models.CharField(
        max_length=10, 
        choices=[("linear", "Linear"), ("logistic", "Logístico")],
        default="linear",
        help_text="Tipo de crecimiento de la tendencia."
    )

    cap_max = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Capacidad máxima (obligatorio si crecimiento = logístico)."
    )

    cap_min = models.FloatField(
        null=True, 
        blank=True,
        help_text="Capacidad mínima opcional en crecimiento logístico."
    )

    int_confianza = models.FloatField(
        default=0.80,
        help_text="Intervalo de confianza (0 a 1)."
    )

    # Estacionalidades
    est_anual = models.BooleanField(
        default=True,
        help_text="Indica si se usará estacionalidad anual."
    )
    fourier_anual = models.IntegerField(
        default=10,
        help_text="Número de complejidad de Fourier para la estacionalidad anual."
    )
    est_semanal = models.BooleanField(
        default=True,
        help_text="Indica si se usará estacionalidad semanal."
    )
    fourier_semanal = models.IntegerField(
        default=3,
        help_text="Número de complejidad de Fourier para la estacionalidad semanal."
    )
    est_diaria = models.BooleanField(
        default=False,
        help_text="Indica si se usará estacionalidad diaria."
    )
    fourier_diaria = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Número de complejidad de Fourier para la estacionalidad diaria."
    )

    modo_est = models.CharField(
        max_length=15,
        choices=[("additive", "Aditiva"), ("multiplicative", "Multiplicativa")],
        default="additive",
        help_text="Tipo de estacionalidad (aditiva o multiplicativa)."
    )

    # Parámetros de Prophet
    scale_est = models.FloatField(
        default=10.0, 
        help_text="Peso de la estacionalidad."
    )
    scale_feriados = models.FloatField(
        default=10.0, 
        help_text="Peso de los feriados/eventos especiales."
    )
    scale_cambio = models.FloatField(
        default=0.05, 
        help_text="Flexibilidad en cambio de tendencia"
    )
    n_cambios = models.IntegerField(
        default=25, 
        help_text="Número de posibles puntos de cambio"
    )
    cambios = models.JSONField(
        default=list, 
        help_text="Lista personalizada de puntos de cambio"
    )

    # Eventos / regresores
    usar_feriados = models.BooleanField(
        default=False, 
        help_text="Indica si se usará feriados/eventos especiales."
    )
    eventos = models.JSONField(
        default=list,
        help_text="Lista de eventos especiales definidos"
    )
    estacionalidades_extra = models.JSONField(
        default=list,
        help_text="Definición de estacionalidades adicionales."
    )
    regresores = models.JSONField(
        default=list,
        help_text="Regresores externos adicionales."
    )

    # Incertidumbre
    inc_tendencia = models.BooleanField(
        default=True, 
        help_text="Indica si se incluirá incertidumbre en la tendencia."
    )
    inc_estacionalidad = models.BooleanField(
        default=True, 
        help_text="Indica si se incluirá incertidumbre en la estacionalidad."
    )

    # Frecuencia de datos
    frecuencia = models.CharField(
        max_length=10,
        choices=[("D", "Diaria"), ("W", "Semanal"), ("M", "Mensual")],
        default="D",
        help_text="Frecuencia de los datos de entrada"
    )

    descripcion = models.TextField(
        null=True, 
        blank=True, 
        help_text="Descripción de la configuración."
    )
    estado = models.BooleanField(
        default=True,
        help_text="Indica si la configuración está activa."
    )

    def clean(self):
        # Intervalo de confianza entre 0 y 1
        if not (0 < self.int_confianza <= 1):
            raise ValidationError("El intervalo de confianza debe estar entre 0 y 1.")

        # Crecimiento logístico requiere capacidad máxima
        if self.crecimiento == "logistic" and self.cap_max is None:
            raise ValidationError("Para crecimiento logístico, se debe definir capacidad máxima.")

        # Fourier positivo si se usan
        if self.est_anual and (self.fourier_anual is None or self.fourier_anual <= 0):
            raise ValidationError("Fourier anual debe ser positivo si se usa.")
        if self.est_semanal and (self.fourier_semanal is None or self.fourier_semanal <= 0):
            raise ValidationError("Fourier semanal debe ser positivo si se usa.")
        if self.est_diaria and (self.fourier_diaria is None or self.fourier_diaria <= 0):
            raise ValidationError("Fourier diaria debe ser positivo si se usa.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Configuración {self.nombre}"

# 🔹 Modelos relacionados con predicciones

class Prediccion(AuditoriaBase):
    inventario = models.ForeignKey('inventarios.Inventario', on_delete=models.CASCADE)
    configuracion = models.ForeignKey(ConfiguracionModelo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    resultado = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        hoy = timezone.now().date()

        if self.fecha_inicio > self.fecha_fin:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        if self.fecha_inicio < hoy or self.fecha_fin < hoy:
            raise ValidationError("Las fechas de predicción no pueden ser anteriores a hoy.")

        if self.resultado < 0:
            raise ValidationError("El resultado de la predicción no puede ser negativo.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prediccion {self.fecha_inicio} - {self.fecha_fin} - {self.inventario.producto.nombre} - {self.configuracion.nombre}"


class DetallePrediccion(models.Model):
    prediccion = models.ForeignKey(Prediccion, on_delete=models.CASCADE, related_name='detalles')
    cantidad = models.IntegerField()
    fecha = models.DateField()

    # Comprueba que la cantidad predicha no sea negativa.
    def clean(self):
        if self.cantidad < 0:
            raise ValidationError("La cantidad predicha no puede ser negativa.")

        # Comprueba que la fecha del detalle está dentro del rango de la predicción.
        if not (self.prediccion.fecha_inicio <= self.fecha <= self.prediccion.fecha_fin):
            raise ValidationError("La fecha del detalle debe estar dentro del rango de la predicción.")

    # Guarda el detalle de la predicción después de haber comprobado su validez.
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    # Devuelve una representación en cadena del objeto.
    def __str__(self):
        return f"Detalle Prediccion {self.fecha} - {self.prediccion.inventario.producto.nombre} - {self.prediccion.configuracion.nombre}"
