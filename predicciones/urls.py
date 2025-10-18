# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrediccionViewSet, PrediccionCSV, DetallePrediccionViewSet, ConfiguracionModeloViewSet, ConfigModelSelectIDViewSet

# Configuramos el router para las predicciones
router = DefaultRouter()
router.register(r'predicciones', PrediccionViewSet)
router.register(r'detalles-predicciones', DetallePrediccionViewSet)
router.register(r'configuraciones-modelo', ConfiguracionModeloViewSet)
router.register(r'config-model-select-id', ConfigModelSelectIDViewSet, basename='config-model-select-id')

urlpatterns = [
    # URL para la vista de predicción CSV
    path('prediccion/csv/', PrediccionCSV.as_view(), name='prediccion_csv'),
    
    # Rutas generadas automáticamente por el router
    path('', include(router.urls)),  # Utiliza una ruta base como api/v1/
]
