from django.urls import path, include, re_path
from rest_framework import routers
from .views import CategoriaView, ProveedorView, ProductoView, ProductoHistoryView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = routers.DefaultRouter()

router.register(r'categorias', CategoriaView)  # Rutas para manejar categorías
router.register(r'productos', ProductoView)  # Rutas para manejar productos
router.register(r'proveedores', ProveedorView)  # Rutas para manejar proveedores

schema_view = get_schema_view(
   openapi.Info(
      title="Productos API",
      default_version='v1',
      description="Documentación de la API de Productos",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@local.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path("", include(router.urls)),

   # 👇 Nueva ruta para el historial del producto
   path('productos/<int:pk>/historial/', ProductoHistoryView.as_view(), name='producto-historial'),

   # swagger
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
