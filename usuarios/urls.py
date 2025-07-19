from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views
from .views import *

router = DefaultRouter()
router.register('usuario', UsuarioViewSet, basename='usuario')
router.register('rol', RolViewSet, basename="rol")

login_view = LoginViewset.as_view({'post': 'create'})

urlpatterns = [
    path('', include(router.urls)),  # Usa el router para recursos CRUD
    path('login/', login_view, name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]
