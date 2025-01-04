# from django.urls import path, include, re_path
# from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, RoleViewSet, UserRoleViewSet
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework import permissions

# router = DefaultRouter()
# router.register(r'usuarios', UserViewSet)
# router.register(r'roles', RoleViewSet)
# router.register(r'rolesUsuario', UserRoleViewSet)

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Usuarios API",
#       default_version='v1',
#       description="Documentación de la API de Usuarios",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@local.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

# urlpatterns = [
#     path("", include(router.urls)),
#     re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]

from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()
router.register('register', RegisterViewset, basename='register')
router.register('login', LoginViewset, basename='login')
router.register('users', UserViewset, basename='users')
urlpatterns = router.urls

