from django.urls import path, include, re_path
from rest_framework import routers
from .views import VentaViewSet, DetalleVentaViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = routers.DefaultRouter()
router.register(r'ventas', VentaViewSet)
router.register(r'detalles_venta', DetalleVentaViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Ventas API",
      default_version='v1',
      description="Documentación de la API de Ventas",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@local.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include(router.urls)),  # Rutas de la API
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
