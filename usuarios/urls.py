from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

from .views import (
    GroupViewSet,
    PermissionViewSet,
    UsuarioViewSet,
    LoginViewset,
    UsuarioListViewSet,
    RolSelectDualViewSet,
    RolListViewSet,
)

router = DefaultRouter()
router.register('grupos', GroupViewSet, basename="grupo")
router.register('permisos', PermissionViewSet, basename="permiso")
router.register('usuarios', UsuarioViewSet, basename='usuario')
router.register('rol-select-dual', RolSelectDualViewSet, basename='rol-select-dual')

login_view = LoginViewset.as_view({'post': 'create'})

urlpatterns = [
    # CRUD para grupos, permisos, usuarios y roles
    path('', include(router.urls)),

    # Endpoints para autenticación con Knox
    path('login/', login_view, name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

    # Endpoints para usuarios
    path('usuarios-list/', UsuarioListViewSet.as_view(), name='usuario-list'),
    # Endpoints para roles
    path('roles-list/', RolListViewSet.as_view(), name='rol-list'),
]
