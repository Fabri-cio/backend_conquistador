from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrediccionViewSet

router = DefaultRouter()
router.register(r'predicciones', PrediccionViewSet)

urlpatterns = [ 
    path('', include(router.urls)),
]