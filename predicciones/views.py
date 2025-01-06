from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Prediccion
from .serializers import PrediccionSerializer

class PrediccionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD del modelo Prediccion.
    """
    queryset = Prediccion.objects.all().order_by('-fecha_prediccion')  # Ordenar por fecha descendente
    serializer_class = PrediccionSerializer
    permission_classes = [IsAuthenticated]  # Asegura que solo usuarios autenticados accedan a la API

    def perform_create(self, serializer):
        """
        Personaliza la creación de la predicción para asignar automáticamente
        el usuario responsable basado en el usuario autenticado.
        """
        serializer.save(usuario_responsable=self.request.user)
