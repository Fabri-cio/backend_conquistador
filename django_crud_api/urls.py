"""
URL configuration for django_crud_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from knox import views as knox_views

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
    path('api/v1/almacenes/', include(('almacenes.urls', 'almacenes'), namespace='almacenes')),
    path('api/v1/predicciones/', include(('predicciones.urls', 'predicciones'), namespace='predicciones')),

    #path('api/auth/',include('knox.urls')), 

    path('logout/',knox_views.LogoutView.as_view(), name='knox_logout'), 
    path('logoutall/',knox_views.LogoutAllView.as_view(), name='knox_logoutall'), 
    path('api/password_reset/',include('django_rest_passwordreset.urls', namespace='password_reset')), 

]
