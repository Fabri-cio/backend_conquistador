from rest_framework import serializers
from .models import Cliente, Venta, DetalleVenta
from productos.serializer import ProductoSerializer

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    # cliente = ClienteSerializer()
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())  # Solo el ID del cliente

    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    # venta = VentaSerializer()
    venta = serializers.PrimaryKeyRelatedField(queryset=Venta.objects.all())  # Solo el ID de la venta
    producto = ProductoSerializer()

    class Meta:
        model = DetalleVenta
        fields = '__all__'