# Django REST Framework
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

# Django
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group, Permission

# Terceros
from knox.models import AuthToken

# Proyecto local
from .serializers import (
    UsuarioSerializer,
    LoginSerializer,
    GroupSerializer,
    PermissionSerializer,
)
from .models import Usuario
from django_crud_api.mixins import PaginacionYAllDataMixin

User = get_user_model()

class GroupViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    """
    CRUD completo para Grupos y asignación de permisos
    """
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated] # Así cualquiera puede ver

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listar y detallar permisos disponibles
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    # permission_classes = [permissions.IsAuthenticated]

class LoginViewset(viewsets.ViewSet):
    """
    Endpoint para login con autenticación vía email y contraseña usando Knox
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                _, token = AuthToken.objects.create(user)
                return Response({
                    "user": self.serializer_class(user).data,
                    "token": token
                })
            else:
                return Response({"error": "Invalid credentials"}, status=401)
        else:
            return Response(serializer.errors, status=400)

class UsuarioViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    """
    CRUD para usuarios, con paginación y opción para traer todos sin paginar
    """
    serializer_class = UsuarioSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Usuario.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        all_data = request.query_params.get('all_data', 'false').lower() == 'true'
        if all_data:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)
