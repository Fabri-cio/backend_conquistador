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
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from core.views import AuditableModelViewSet


# PrediccionCSV hace un procesamiento especial (entrenar modelo, recibir archivo).
class PrediccionCSV(APIView):
    """
    API para recibir un CSV y un modelo_id opcional,
    entrenar Prophet usando la configuración guardada y devolver la predicción.
    """

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        config_data = request.data.get('config', None)

        if not file:
            return JsonResponse({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Leer CSV
            df = pd.read_csv(file)
            if not set(['ds', 'y']).issubset(df.columns):
                return JsonResponse({"error": "CSV inválido. Debe contener columnas 'ds' y 'y'."}, status=status.HTTP_400_BAD_REQUEST)

            df['ds'] = pd.to_datetime(df['ds'])
            df['y'] = pd.to_numeric(df['y'], errors='coerce')
            if df['y'].isnull().any():
                return JsonResponse({"error": "Columna 'y' contiene datos inválidos."}, status=status.HTTP_400_BAD_REQUEST)

            # Manejo seguro de config
            modelo_id = None
            periodos_prediccion = 7
            if config_data:
                if isinstance(config_data, str):
                    config_data = json.loads(config_data)
                modelo_id = config_data.get("modelo_id", None)
                periodos_prediccion = config_data.get("periodos_prediccion", periodos_prediccion)

            if not modelo_id:
                return JsonResponse({"error": "Se requiere modelo_id"}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener configuración de la DB
            try:
                config_modelo = ConfiguracionModelo.objects.get(id=modelo_id)
            except ConfiguracionModelo.DoesNotExist:
                return JsonResponse({"error": "Configuración de modelo no encontrada"}, status=status.HTTP_404_NOT_FOUND)

            # Si el crecimiento es logístico, agregar columnas 'cap' y 'floor'
            if config_modelo.crecimiento == "logistic":
                if config_modelo.cap_max is None:
                    return JsonResponse({"error": "cap_max es obligatorio para crecimiento logístico."}, status=status.HTTP_400_BAD_REQUEST)
                
                df['cap'] = config_modelo.cap_max
                df['floor'] = config_modelo.cap_min if config_modelo.cap_min is not None else 0

            # Configuración de Prophet usando el modelo guardado
            prophet_params = {
                "growth": config_modelo.crecimiento,
                "seasonality_mode": config_modelo.modo_est,
                "changepoint_prior_scale": config_modelo.scale_cambio,
                "seasonality_prior_scale": config_modelo.scale_est,
                "holidays_prior_scale": config_modelo.scale_feriados,
                "yearly_seasonality": config_modelo.fourier_anual if config_modelo.est_anual else False,
                "weekly_seasonality": config_modelo.fourier_semanal if config_modelo.est_semanal else False,
                "daily_seasonality": config_modelo.fourier_diaria if config_modelo.est_diaria else False,
                "holidays": None  # opcional, puedes incluir config_modelo.eventos
            }

            # Crear y entrenar modelo Prophet
            m = Prophet(**prophet_params)
            m.fit(df)

            # Crear dataframe futuro y predecir
            future = m.make_future_dataframe(periods=periodos_prediccion)
            if config_modelo.crecimiento == "logistic":
                future['cap'] = config_modelo.cap_max
                future['floor'] = config_modelo.cap_min if config_modelo.cap_min is not None else 0

            forecast = m.predict(future)

            # Devolver los últimos n días
            forecast_result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periodos_prediccion).to_dict(orient="records")
            return Response({"forecast": forecast_result}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PrediccionViewSet maneja las operaciones CRUD del modelo Prediccion.
class PrediccionViewSet(PaginacionYAllDataMixin, AuditableModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD del modelo Prediccion.
    """
    queryset = Prediccion.objects.all().order_by('id')
    serializer_class = PrediccionSerializer
    permission_classes = [permissions.AllowAny]  # Asegura que solo usuarios autenticados accedan a la API

# DetallePrediccionViewSet maneja las operaciones CRUD del modelo DetallePrediccion.
class DetallePrediccionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD del modelo DetallePrediccion.
    """
    queryset = DetallePrediccion.objects.all().order_by('id')
    serializer_class = DetallePrediccionSerializer
    permission_classes = [permissions.AllowAny]  # Asegura que solo usuarios autenticados accedan a la API

# ConfiguracionModeloViewSet maneja las operaciones CRUD del modelo ConfiguracionModelo.
class ConfiguracionModeloViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD del modelo ConfiguracionModelo.
    """
    queryset = ConfiguracionModelo.objects.all().order_by('id')    
    serializer_class = ConfiguracionModeloSerializer
    permission_classes = [permissions.AllowAny]  # Asegura que solo usuarios autenticados accedan a la API