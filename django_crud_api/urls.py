from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Documentación de la API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@local.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/productos/', include(('productos.urls', 'productos'), namespace='productos')),
    path('api/v1/ventas/', include(('ventas.urls', 'ventas'), namespace='ventas')),
    path('api/v1/usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('api/v1/inventarios/', include(('inventarios.urls', 'inventarios'), namespace='inventarios')),
    path('api/v1/predicciones/', include(('predicciones.urls', 'predicciones'), namespace='predicciones')),
    path('api/v1/compras/', include(('compras.urls', 'compras'), namespace='compras')),
    path('api/v1/reportes/', include(('reportes.urls', 'reportes'), namespace='reportes')),


    # Password Reset (en su propia app opcionalmente)
    path('api/v1/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')), 

    # Documentación Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
