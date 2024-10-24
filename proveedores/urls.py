from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import ProveedorView, OrdenCompraView, DetalleOrdenView

router = routers.DefaultRouter()

router.register(r'proveedores', ProveedorView)  # Rutas para proveedores
router.register(r'ordenes', OrdenCompraView)  # Rutas para ordenes de compra
router.register(r'detalles-ordenes', DetalleOrdenView)  # Rutas para detalles de la orden

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include_docs_urls(title="Proveedores API"))
]
