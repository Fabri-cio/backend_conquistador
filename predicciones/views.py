import json
import pandas as pd
from prophet import Prophet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.http import JsonResponse
from .models import Prediccion, DetallePrediccion, ConfiguracionModelo
from .serializers import PrediccionSerializer, DetallePrediccionSerializer, ConfiguracionModeloSerializer
from django_crud_api.mixins import PaginacionYAllDataMixin

# PrediccionCSV hace un procesamiento especial (entrenar modelo, recibir archivo).
class PrediccionCSV(APIView):
    """
    API para recibir un CSV y una configuración opcional de Prophet,
    entrenar y devolver la predicción.
    """

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        config = request.data.get('config', None)

         # === DEBUG: mostrar en consola la configuración recibida ===
        print("===== CONFIG RECIBIDA =====")
        print(config)
        print("Tipo:", type(config))
        print("============================")

        if not file:
            return JsonResponse({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Leer CSV
            df = pd.read_csv(file)
            
            # Validar columnas
            if not set(['ds', 'y']).issubset(df.columns):
                return JsonResponse({"error": "Invalid CSV format. Ensure columns 'ds' and 'y' are present."}, status=status.HTTP_400_BAD_REQUEST)

            df['ds'] = pd.to_datetime(df['ds'])
            df['y'] = pd.to_numeric(df['y'], errors='coerce')
            if df['y'].isnull().any():
                return JsonResponse({"error": "Invalid data in 'y' column"}, status=status.HTTP_400_BAD_REQUEST)

            # Configuración por defecto de Prophet
            prophet_params = {
                "growth": "linear",
                "seasonality_mode": "additive",
                "yearly_seasonality": "auto",
                "weekly_seasonality": "auto",
                "daily_seasonality": "auto",
                "holidays": None,
                "changepoint_prior_scale": 0.05,
                "seasonality_prior_scale": 10.0,
                "holidays_prior_scale": 10.0,
            }

            periodos_prediccion = 30  # Valor por defecto

            # Manejo seguro de configuración
            config_data = {}
            if config:
                try:
                    if isinstance(config, str):
                        config_data = json.loads(config)
                    elif isinstance(config, dict):
                        config_data = config
                except Exception:
                    config_data = {}

            # Sobrescribir valores por defecto si existen
            prophet_params["growth"] = config_data.get("modo_crecimiento", prophet_params["growth"])
            prophet_params["seasonality_mode"] = config_data.get("estacionalidad_modo", prophet_params["seasonality_mode"])
            prophet_params["changepoint_prior_scale"] = config_data.get("changepoint_prior_scale", prophet_params["changepoint_prior_scale"])
            prophet_params["seasonality_prior_scale"] = config_data.get("seasonality_prior_scale", prophet_params["seasonality_prior_scale"])
            prophet_params["holidays_prior_scale"] = config_data.get("holidays_prior_scale", prophet_params["holidays_prior_scale"])

            # Fourier personalizado
            yearly = config_data.get("fourier_anual", 0) if config_data.get("usar_est_anual", False) else 0
            weekly = config_data.get("fourier_semanal", 0) if config_data.get("usar_est_semanal", False) else 0
            daily = config_data.get("fourier_diaria", 0) if config_data.get("usar_est_diaria", False) else 0

            prophet_params["yearly_seasonality"] = yearly if yearly > 0 else False
            prophet_params["weekly_seasonality"] = weekly if weekly > 0 else False
            prophet_params["daily_seasonality"] = daily if daily > 0 else False

            # Periodos de predicción
            periodos_prediccion = config_data.get("periodos_prediccion", periodos_prediccion)

            # Crear y entrenar modelo
            m = Prophet(**prophet_params)
            m.fit(df)

            # Crear dataframe futuro y predecir
            future = m.make_future_dataframe(periods=periodos_prediccion)
            forecast = m.predict(future)

            return Response({
                "forecast": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periodos_prediccion).to_dict(orient="records"),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# PrediccionViewSet maneja las operaciones CRUD del modelo Prediccion.
class PrediccionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD del modelo Prediccion.
    """
    queryset = Prediccion.objects.all().order_by('-fecha_prediccion')  # Ordenar por fecha descendente
    serializer_class = PrediccionSerializer
    permission_classes = [permissions.AllowAny]  # Asegura que solo usuarios autenticados accedan a la API

    def perform_create(self, serializer):
        """
        Personaliza la creación de la predicción para asignar automáticamente
        el usuario responsable basado en el usuario autenticado.
        """
        serializer.save(usuario_responsable=self.request.user)

# DetallePrediccionViewSet maneja las operaciones CRUD del modelo DetallePrediccion.
class DetallePrediccionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD del modelo DetallePrediccion.
    """
    queryset = DetallePrediccion.objects.all().order_by('id')  # Ordenar por fecha descendente
    serializer_class = DetallePrediccionSerializer
    permission_classes = [permissions.AllowAny]  # Asegura que solo usuarios autenticados accedan a la API

# ConfiguracionModeloViewSet maneja las operaciones CRUD del modelo ConfiguracionModelo.
class ConfiguracionModeloViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD del modelo ConfiguracionModelo.
    """
    queryset = ConfiguracionModelo.objects.all()  # Ordenar por fecha descendente
    serializer_class = ConfiguracionModeloSerializer
    permission_classes = [permissions.AllowAny]  # Asegura que solo usuarios autenticados accedan a la API