from rest_framework import serializers
from .models import Categoria, Proveedor, Producto
from django.utils.translation import gettext_lazy as _
from .mixins import ImageThumbMixinSerializer

# ---------------------
# Categoria & Proveedor
# ---------------------

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

# ---------------------
# Historial
# ---------------------

class ProductoHistorySerializer(serializers.ModelSerializer):
    history_type = serializers.CharField()
    history_date = serializers.DateTimeField()
    history_user = serializers.SerializerMethodField()
    cambios = serializers.SerializerMethodField()

    class Meta:
        model = Producto.history.model
        fields = [
            'id',
            'nombre',
            'precio',
            'history_type',
            'history_date',
            'history_user',
            'cambios',
        ]

    def get_history_user(self, obj):
        return str(obj.history_user) if obj.history_user else None

    def get_cambios(self, obj):
        previous = obj.prev_record
        if not previous:
            return None
        delta = obj.diff_against(previous)
        cambios = {}
        for change in delta.changes:
            cambios[change.field] = {
                "de": change.old,
                "a": change.new,
            }
        return cambios

# ---------------------
# Productos por Categoria
# ---------------------
class ProductosParaCategoriaSerializer(serializers.ModelSerializer):
    marca = serializers.CharField(source="proveedor.marca", read_only=True)
    class Meta:
        model = Producto
        fields = [
            "id",
            "estado",
            "nombre",
            "precio",
            "imagen",
            "marca",
        ]


class ProductosPorCategoriaSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = [
            "id",
            "nombre",
            "productos",
        ]
    
    def get_productos(self, obj):
        productos = Producto.objects.filter(categoria=obj.id)
        # Asegúrate de pasar el request explícitamente
        request = self.context.get('request')
        serializer = ProductosParaCategoriaSerializer(productos, many=True, context={'request': request})
        return serializer.data

# ---------------------
# Productos por Proveedor
# ---------------------
class ProductosParaProveedorSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source="categoria.nombre", read_only=True)
    class Meta:
        model = Producto
        fields = [
            "id",
            "estado",
            "nombre",
            "precio",
            "imagen",
            "categoria",
        ]

class ProductosPorProveedorSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Proveedor
        fields = [
            "id",
            "marca",
            "productos",
        ]
    
    def get_productos(self, obj):
        productos = Producto.objects.filter(proveedor=obj.id)
        # Asegúrate de pasar el request explícitamente
        request = self.context.get('request')
        serializer = ProductosParaProveedorSerializer(productos, many=True, context={'request': request})
        return serializer.data

#-------------------------
#       listas
#------------------------
class CategoriaListSerializer(ImageThumbMixinSerializer, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = [
            "id",
            "estado",
            "nombre",
            "image_url",
        ]

class ProveedorListSerializer(ImageThumbMixinSerializer, serializers.ModelSerializer):    
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Proveedor
        fields = [
            "id",
            "estado",
            "marca",
            "contacto",
            "telefono",
            "image_url",
        ]

class ProductoListSerializer(ImageThumbMixinSerializer, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    marca_proveedor = serializers.CharField(source="proveedor.marca", read_only=True)
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id",
            "estado",
            "nombre",
            "marca_proveedor",
            "categoria_nombre",
            "precio",
            "image_url",
        ]

class CategoriaSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]

class ProveedorSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ["id", "marca"]

class ProductoSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "nombre"]

class ProveedorPedidosSerializer(ImageThumbMixinSerializer, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Proveedor
        fields = ["id", "image_url", "marca"]