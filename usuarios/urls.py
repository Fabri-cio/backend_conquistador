from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

from .views import (
    GroupViewSet,
    PermissionViewSet,
    UsuarioViewSet,
    LoginViewset,
)

router = DefaultRouter()
router.register('grupos', GroupViewSet, basename="grupo")
router.register('permisos', PermissionViewSet, basename="permiso")
router.register('usuarios', UsuarioViewSet, basename='usuario')

login_view = LoginViewset.as_view({'post': 'create'})

urlpatterns = [
    # CRUD para grupos, permisos, usuarios y roles
    path('', include(router.urls)),

    # Endpoints para autenticación con Knox
    path('login/', login_view, name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]
