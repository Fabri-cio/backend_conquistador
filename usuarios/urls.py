from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, UserRoleViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'rolesUsuario', UserRoleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include_docs_urls(title="Usuarios API"))
]
