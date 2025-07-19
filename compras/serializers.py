from rest_framework import serializers
from .models import Pedido, DetallePedido, RecepcionPedido, DetalleRecepcion, Compra


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'


class RecepcionPedidoSerializer(serializers.ModelSerializer):
    detalles = DetalleRecepcionSerializer(many=True)

    class Meta:
        model = RecepcionPedido
        fields = '__all__'


class DetalleRecepcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleRecepcion
        fields = '__all__'


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'

