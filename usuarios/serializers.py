from rest_framework import serializers

from almacenes.models import Almacen 
from .models import * 
from django.contrib.auth import get_user_model 
User = get_user_model()

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
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

    name_rol = serializers.CharField(source="rol.name", read_only=True)
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    name_rol = serializers.CharField(source="rol.name", read_only=True)
    name_work = serializers.CharField(source="lugar_de_trabajo.nombre", read_only=True)
    class Meta:
        model = Usuario
        fields = [
            'id',
            'email',
            'password',
            'new_password',
            'first_name',
            'last_name',
            'is_superuser',
            'is_active',
            'date_joined',
            'birthday',
            'username',
            'lugar_de_trabajo',
            'name_work',
            'rol',  # Asegúrate de agregar 'rol' aquí
            'name_rol'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'new_password': {'write_only': True, 'required': False},  # 👈 Extra seguridad
        }

    def create(self, validated_data):
        if not validated_data.get('password'):
            raise serializers.ValidationError({'password': 'Este campo es requerido para crear un usuario.'})
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        if new_password:
            instance.set_password(new_password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  
        instance.save()
        return instance