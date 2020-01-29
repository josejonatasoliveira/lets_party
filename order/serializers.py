from rest_framework import serializers

from projeto_tg.evento.models import Evento
from projeto_tg.order.models import Order, OrderItem, Ticket

from projeto_tg.evento.serializers import UploadSessionSerializer, EventoSerializer


class TicketSerializer(serializers.Serializer):
  key = serializers.CharField(read_only=True)
  value = serializers.CharField(read_only=True)

  def create(self, validated_data):
    return Ticket(**validated_data)


class OrderSerializer(serializers.Serializer):
  final_value = serializers.DecimalField(max_digits=10, decimal_places=2)
  upload_session = UploadSessionSerializer()

  def create(self, validated_data):
    return Order(**validated_data)

class OrderItemSerializer(serializers.Serializer):
  order = OrderSerializer()
  event = EventoSerializer()
  ticket = TicketSerializer()
  quantity = serializers.IntegerField()
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  final_price = serializers.DecimalField(max_digits=10, decimal_places=2)

  def create(self, validated_data):
    return OrderItem(**validated_data)