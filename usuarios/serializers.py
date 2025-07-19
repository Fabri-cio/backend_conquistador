# ===========================
# SERIALIZERS.PY ORDENADO Y COMENTADO
# ===========================

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

# Terceros
from rest_framework import serializers

# Proyecto local
from almacenes.models import Almacen 
from .models import Rol, Usuario

User = get_user_model()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField()
    lugar_de_trabajo = serializers.PrimaryKeyRelatedField(
        queryset=Almacen.objects.all(),
        source='lugar_de_trabajo_id',
        required=False
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
    group_names = serializers.SerializerMethodField()
    permission_names = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'password', 'new_password', 'first_name', 'last_name',
            'is_superuser', 'is_staff', 'user_permissions', 'groups', 'is_active',
            'date_joined', 'birthday', 'username', 'lugar_de_trabajo', 'name_work',
            'rol', 'name_rol', 'group_names', 'permission_names'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'new_password': {'write_only': True, 'required': False},
        }

    def get_group_names(self, obj):
        return [group.name for group in obj.groups.all()]

    def get_permission_names(self, obj):
        return list(obj.get_all_permissions())

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