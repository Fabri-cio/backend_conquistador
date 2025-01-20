import pandas as pd
from prophet import Prophet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.http import JsonResponse
from .models import Prediccion
from productos.models import Producto
from usuarios.models import CustomUser
from .serializers import PrediccionSerializer


class PrediccionCSV(APIView):
    # """
    # Vista para realizar la predicción a partir de un archivo CSV.
    # """
    # def post(self, request, *args, **kwargs):
    #     file = request.FILES.get('file')  # Obtener el archivo CSV enviado desde el frontend

    #     if not file:
    #         return JsonResponse({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    #     # Leer el archivo CSV
    #     df = pd.read_csv(file)
        
    #     # Asegúrate de que el DataFrame tenga las columnas correctas
    #     if not set(['ds', 'y']).issubset(df.columns):
    #         return JsonResponse({"error": "Invalid CSV format. Ensure columns 'ds' and 'y' are present."}, status=status.HTTP_400_BAD_REQUEST)
        
    #     # Configurar el modelo Prophet
    #     m = Prophet()
    #     m.fit(df)

    #     # Crear el dataframe futuro para hacer la predicción
    #     future = m.make_future_dataframe(df, periods=30)  # Aquí ajustas el periodo a predecir
    #     forecast = m.predict(future)

    #     # Guardar el resultado de la predicción en la base de datos
    #     producto = Producto.objects.first()  # Puedes ajustar esto para obtener el producto específico
    #     usuario = CustomUser.objects.first()  # Ajustar para el usuario que realiza la predicción

    #     prediccion = Prediccion(
    #         producto=producto,
    #         usuario_responsable=usuario,
    #         resultado_prediccion=forecast['yhat'].iloc[-1],  # Se puede ajustar para obtener el valor deseado
    #         model_used="Prophet"
    #     )
    #     prediccion.save()

    #     return Response({
    #         "forecast": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail().to_dict(orient="records"),
    #         "prediccion_id": prediccion.id_prediccion
    #     }, status=status.HTTP_200_OK)

   def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return JsonResponse({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Leer el archivo CSV
            df = pd.read_csv(file)
            
            # Validar columnas
            if not set(['ds', 'y']).issubset(df.columns):
                return JsonResponse({"error": "Invalid CSV format. Ensure columns 'ds' and 'y' are present."}, status=status.HTTP_400_BAD_REQUEST)

            # Convertir columnas a tipos adecuados
            df['ds'] = pd.to_datetime(df['ds'])
            df['y'] = pd.to_numeric(df['y'], errors='coerce')
            if df['y'].isnull().any():
                return JsonResponse({"error": "Invalid data in 'y' column"}, status=status.HTTP_400_BAD_REQUEST)

            # Configurar y entrenar el modelo Prophet
            m = Prophet()
            m.fit(df)

            # Crear el dataframe futuro y hacer predicción
            future = m.make_future_dataframe(periods=30)  # Aquí ajustas el periodo a predecir
            forecast = m.predict(future)

            # Devolver resultados de la predicción
            return Response({
                "forecast": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30).to_dict(orient="records"),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
