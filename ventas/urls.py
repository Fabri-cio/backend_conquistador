from django.urls import path, include
from rest_framework import routers
from .views import VentaViewSet, DetalleVentaViewSet
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r'ventas', VentaViewSet)
router.register(r'detalles_venta', DetalleVentaViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Rutas de la API
     path("docs/", include_docs_urls(title="Ventas API"))
]
