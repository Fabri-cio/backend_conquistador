from rest_framework import serializers

from almacenes.models import Almacen 
from .models import * 
from django.contrib.auth import get_user_model 
User = get_user_model()

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

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
    
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'birthday', 'lugar_de_trabajo','role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        lugar_de_trabajo = validated_data.pop('lugar_de_trabajo', None)  # Manejar el campo opcional
        user = User.objects.create_user(**validated_data)

        role = validated_data.pop('role', None)

        # Si el campo lugar_de_trabajo es proporcionado, actualiza el usuario con él
        if lugar_de_trabajo:
            user.lugar_de_trabajo = lugar_de_trabajo
            user.save()

        # Asignar el rol al usuario
        if role:
            user.role = role
            user.save()

        return user

class CustomUserSerializer(serializers.ModelSerializer):
    name_rol = serializers.CharField(source="role.name", read_only=True)
    name_work = serializers.CharField(source="lugar_de_trabajo.nombre", read_only=True)
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
            'name_work',
            'role',  # Asegúrate de agregar 'role' aquí
            'name_rol'
        ]


