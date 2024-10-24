from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import InventarioView

router = routers.DefaultRouter()

# router.register(r'inventario', views.InventarioView, 'inventario') #el tercer argumento no es necesario
router.register(r'inventario', InventarioView)

urlpatterns = [
    # path("api/v1/", include(router.urls)),
    path("", include(router.urls)),
    path("docs/", include_docs_urls(title="Inventario API"))
]
