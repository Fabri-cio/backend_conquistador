from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from .views import AlmacenOTiendaViewSet, InventarioViewSet, TipoMovimientoViewSet, MovimientoViewSet

router = DefaultRouter()
router.register(r'almacenes', AlmacenOTiendaViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'tiposMovimiento', TipoMovimientoViewSet)
router.register(r'movimientos', MovimientoViewSet)

urlpatterns = [
    path("", include(router.urls)), 
    path("docs/", include_docs_urls(title="Almacenes API"))
]