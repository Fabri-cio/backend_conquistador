# ===========================
# SERIALIZERS.PY ORDENADO Y COMENTADO
# ===========================

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

# Terceros
from rest_framework import serializers

# Proyecto local
from inventarios.models import Almacen 
from .models import Usuario

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

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField()
    lugar_de_trabajo = serializers.PrimaryKeyRelatedField(
        queryset=Almacen.objects.all(),
        source='lugar_de_trabajo_id',
        required=False
    )

    rol = serializers.SerializerMethodField()

    def get_rol(self, obj):
        group = obj.groups.first()
        return group.name if group else None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    rol = serializers.SerializerMethodField()
    name_work = serializers.CharField(source="lugar_de_trabajo.nombre", read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'password', 'new_password', 'first_name', 'last_name',
            'is_superuser', 'is_staff', 'is_active',
            'date_joined', 'birthday', 'username', 'lugar_de_trabajo', 'name_work',
            'rol',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'new_password': {'write_only': True, 'required': False},
        }

    def get_rol(self, obj):
        group = obj.groups.first()
        return group.name if group else None

    def create(self, validated_data):
        rol_id = self.initial_data.get("rol")  # <- ID del grupo que envía el frontend
        password = validated_data.pop("password", None)
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        if rol_id:
            try:
                group = Group.objects.get(id=rol_id)
                user.groups.set([group])  # Asignar el grupo
            except Group.DoesNotExist:
                raise serializers.ValidationError({"rol": "El grupo especificado no existe."})

        return user

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        if new_password:
            instance.set_password(new_password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  
        instance.save()

        rol_id = self.initial_data.get("rol")
        if rol_id:
            try:
                group = Group.objects.get(id=rol_id)
                instance.groups.set([group])
            except Group.DoesNotExist:
                raise serializers.ValidationError({"rol": "El grupo especificado no existe."})

        return instance