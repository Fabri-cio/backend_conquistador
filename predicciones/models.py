from email.policy import default
from django.db import models
from django.core.exceptions import ValidationError
from core.models import AuditoriaBase

# 🔥 Configuracion de Prophet
class ConfiguracionModelo(models.Model):
    nombre_config = models.CharField(max_length=100)

    # Crecimiento y saturación
    modo_crecimiento = models.CharField(
        max_length=10, 
        choices=[("linear", "Linear"), ("logistic", "Logistic")]
    )
    capacidad_maxima = models.FloatField(null=True, blank=True)
    capacidad_minima = models.FloatField(null=True, blank=True)

    # Intervalos
    intervalo_confianza = models.FloatField(default=0.80)

    # Estacionalidades estandar
    usar_est_anual = models.BooleanField(default=True)
    fourier_anual = models.IntegerField(default=10)
    usar_est_semanal = models.BooleanField(default=True)
    fourier_semanal = models.IntegerField(default=3)
    usar_est_diaria = models.BooleanField(default=False)
    fourier_diaria = models.IntegerField(null=True, blank=True)

    # Modo estacionalidad
    estacionalidad_modo = models.CharField(max_length=15, choices=[("additive", "Aditiva"), ("multiplicative", "Multiplicativa")], default="additive")

    # Prior scales
    seasonality_prior_scale = models.FloatField(default=10.0)
    holidays_prior_scale = models.FloatField(default=10.0)
    changepoint_prior_scale = models.FloatField(default=0.05)

    # Puntos de cambio
    n_changepoints = models.IntegerField(default=25)
    changepoints = models.JSONField(default=list)

    # Feriados y eventos especiales
    usar_feriados = models.BooleanField(default=False)
    eventos_especiales = models.JSONField(default=list)
    estacionalidades_personalizadas = models.JSONField(default=list)

    # Regresores adicionales
    regresores_adicionales = models.JSONField(default=list)

    # Configuración de incertidumbre
    incluir_incertidumbre_tendencia = models.BooleanField(default=True)
    incluir_incertidumbre_estacionalidad = models.BooleanField(default=True)
    
    # Frecuencia de datos
    frecuencia_datos = models.CharField(
        max_length=10, 
        choices=[
            ("D", "Diaria"), 
            ("W", "Semanal"), 
            ("M", "Mensual")
        ],
        default="D"
    )

    # Validacion cruzada
    usar_validacion_cruzada = models.BooleanField(default=False)
    horizonte_cv = models.IntegerField(default=30)
    periodo_cv = models.IntegerField(default=15)

    def get_prophet_params(self):
        """
        Devuelve un diccionario con los parámetros listos para crear un modelo Prophet
        según la configuración actual.
        """
        params = {
            "growth": self.modo_crecimiento,
            "changepoint_prior_scale": self.changepoint_prior_scale,
            "seasonality_prior_scale": self.seasonality_prior_scale,
            "holidays_prior_scale": self.holidays_prior_scale,
            "interval_width": self.intervalo_confianza,
            "weekly_seasonality": self.usar_est_semanal,
            "yearly_seasonality": self.usar_est_anual,
            "daily_seasonality": self.usar_est_diaria,
        }

        # Si el crecimiento es logístico, añadir capacidad
        if self.modo_crecimiento == "logistic":
            params["cap"] = self.capacidad_maxima
            if self.capacidad_minima is not None:
                params["floor"] = self.capacidad_minima

        # Estacionalidades personalizadas
        if self.estacionalidades_personalizadas:
            params["add_seasonality"] = self.estacionalidades_personalizadas

        # Feriados y eventos especiales
        if self.usar_feriados and self.eventos_especiales:
            params["holidays"] = self.eventos_especiales

        return params

    def crear_modelo_prophet(self):
        """
        Crea y devuelve un modelo Prophet configurado según esta configuración.
        """
        params = self.get_prophet_params()
        m = Prophet(**params)

        # Configurar Fourier para estacionalidades manuales si es necesario
        if self.usar_est_anual and self.fourier_anual:
            m.add_seasonality(
                name='yearly', 
                period=365.25, 
                fourier_order=self.fourier_anual,
                mode=self.estacionalidad_modo
            )
        if self.usar_est_semanal and self.fourier_semanal:
            m.add_seasonality(
                name='weekly', 
                period=7, 
                fourier_order=self.fourier_semanal,
                mode=self.estacionalidad_modo
            )
        if self.usar_est_diaria and self.fourier_diaria:
            m.add_seasonality(
                name='daily', 
                period=1, 
                fourier_order=self.fourier_diaria,
                mode=self.estacionalidad_modo
            )

        # Agregar regresores adicionales
        for reg in self.regresores_adicionales:
            # reg debe ser un diccionario con keys: name, prior_scale, mode
            m.add_regressor(
                name=reg.get("name"),
                prior_scale=reg.get("prior_scale", 10.0),
                mode=reg.get("mode", "additive")
            )

        return m
    
    def __str__(self):
        return f"Configuracion {self.nombre_config}"

class Prediccion(AuditoriaBase):
    inventario = models.ForeignKey('inventarios.Inventario', on_delete=models.CASCADE)  # FK a Inventario
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


