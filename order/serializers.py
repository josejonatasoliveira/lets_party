from rest_framework import serializers

from projeto_tg.evento.models import Evento
from projeto_tg.order.models import Order, OrderItem

from projeto_tg.evento.serializers import UploadSessionSerializer, EventoSerializer

class OrderSerializer(serializers.Serializer):
  final_value = serializers.DecimalField(max_digits=10, decimal_places=2)
  upload_session = UploadSessionSerializer()

  def create(self, validated_data):
    return Order(**validated_data)

class OrderItemSerializer(serializers.Serializer):
  order = OrderSerializer()
  event = EventoSerializer()
  quantity = serializers.IntegerField()
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  final_price = serializers.DecimalField(max_digits=10, decimal_places=2)

  def create(self, validated_data):
    breakpoint()
    return OrderItem(**validated_data)