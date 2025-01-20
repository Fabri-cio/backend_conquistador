# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrediccionViewSet, PrediccionCSV

# Configuramos el router para las predicciones
router = DefaultRouter()
router.register(r'predicciones', PrediccionViewSet)

urlpatterns = [
    # URL para la vista de predicción CSV
    path('prediccion/csv/', PrediccionCSV.as_view(), name='prediccion_csv'),
    
    # Rutas generadas automáticamente por el router
    path('', include(router.urls)),  # Utiliza una ruta base como api/v1/
]
