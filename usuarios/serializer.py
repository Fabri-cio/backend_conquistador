from rest_framework import serializers

from almacenes.models import Almacen 
from .models import * 
from django.contrib.auth import get_user_model 
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField()
    lugar_de_trabajo = serializers.PrimaryKeyRelatedField(
        queryset=Almacen.objects.all(),
        source='lugar_de_trabajo_id',
        required=False  # Hacer que el campo sea opcional
    )
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'birthday', 'lugar_de_trabajo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        lugar_de_trabajo = validated_data.pop('lugar_de_trabajo', None)  # Manejar el campo opcional
        user = User.objects.create_user(**validated_data)

        # Si el campo lugar_de_trabajo es proporcionado, actualiza el usuario con él
        if lugar_de_trabajo:
            user.lugar_de_trabajo = lugar_de_trabajo
            user.save()

        return user

class CustomUserSerializer(serializers.ModelSerializer):
    # Acceder a los permisos relacionados con el usuario
    user_permissions = serializers.StringRelatedField(many=True)  # Este es el campo correcto para los permisos
    groups = serializers.StringRelatedField(many=True)  # Mostrar los grupos del usuario como texto

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'date_joined',
            'birthday',
            'username',
            'lugar_de_trabajo',
            'user_permissions',  # Cambié 'permissions' por 'user_permissions'
            'groups',
        ]


