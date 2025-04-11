from rest_framework import viewsets, permissions, status
from .serializer import * 
from .models import * 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model, authenticate
from knox.models import AuthToken
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

# Definir una clase de paginación personalizada si quieres ajustar el tamaño de la página y el comportamiento
class PaginacionPersonalizada(PageNumberPagination):
    page_size = 10  # Número predeterminado de elementos por página
    page_size_query_param = 'page_size'  # Permitir cambiar el tamaño de la página desde los parámetros de la consulta
    max_page_size = 100  # Tamaño máximo de página permitido

class LoginViewset(viewsets.ViewSet):
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
                return Response(
                    {
                        "user": self.serializer_class(user).data,
                        "token": token
                    }
                )
            else: 
                return Response({"error":"Invalid credentials"}, status=401)    
        else: 
            return Response(serializer.errors,status=400)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all().order_by('id')  # Ordena por id_producto en lugar de id

    pagination_class = PaginacionPersonalizada

    def list(self, request, *args, **kwargs):
        all_data = request.query_params.get('all_data', 'false').lower() == 'true'  # Convierte a booleano correctamente

        if all_data:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)  # Usa la paginación normal