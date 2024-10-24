from rest_framework import viewsets
from .models import Usuario
from .serializer import UsuarioSerializer

class UsuarioView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
