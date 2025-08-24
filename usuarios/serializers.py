from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

# Terceros
from rest_framework import serializers

# Proyecto local
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
    # id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField()
    # lugar_de_trabajo = serializers.PrimaryKeyRelatedField(
    #     queryset=Almacen.objects.all(),
    #     source='lugar_de_trabajo_id',
    #     required=False
    # )
    full_name = serializers.SerializerMethodField()
    rol = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    def get_rol(self, obj):
        return [group.name for group in obj.groups.all()]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    roles = serializers.SerializerMethodField()  # Para mostrar múltiples roles
    name_work = serializers.CharField(source="lugar_de_trabajo.nombre", read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'password', 'new_password', 'first_name', 'last_name',
            'is_superuser', 'is_staff', 'is_active',
            'date_joined', 'birthday', 'username', 'lugar_de_trabajo', 'name_work',
            'roles',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'new_password': {'write_only': True, 'required': False},
        }

    def validate_email(self, value):
        # Verifica si otro usuario ya tiene ese email
        user = self.instance  # None si es creación
        if User.objects.filter(email=value).exclude(id=getattr(user, 'id', None)).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value

    def get_roles(self, obj):
        return [{"id": g.id, "name": g.name} for g in obj.groups.all()]

    def create(self, validated_data):
        roles_ids = self.initial_data.get("roles", [])  # IDs enviados desde el frontend
        password = validated_data.pop("password", None)
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        # Asignación de roles con manejo de errores
        try:
            if roles_ids:
                groups = Group.objects.filter(id__in=roles_ids)
                if not groups.exists():
                    raise serializers.ValidationError({"roles": "Ningún rol válido fue encontrado."})
                user.groups.set(groups)
        except Exception as e:
            raise serializers.ValidationError({"roles": f"Error asignando roles: {str(e)}"})

        return user

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        if new_password:
            instance.set_password(new_password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        roles_ids = self.initial_data.get("roles", [])
        # Actualización de roles con manejo de errores
        try:
            if roles_ids:
                groups = Group.objects.filter(id__in=roles_ids)
                if not groups.exists():
                    raise serializers.ValidationError({"roles": "Ningún grupo válido fue encontrado."})
                instance.groups.set(groups)
        except Exception as e:
            raise serializers.ValidationError({"roles": f"Error actualizando roles: {str(e)}"})

        return instance