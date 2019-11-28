from django.shortcuts import get_object_or_404

from projeto_tg.evento.models import Evento, UploadSession
from projeto_tg.cart.views import cart_remove
from .models import Order, OrderItem

def checkout_order(
  cart=None,
  user=None):

  upload_session = UploadSession.objects.create(user=user)

  for item in cart.__iter__():

    order, has_create = Order.objects.get_or_create(
      final_value=item['total_price'],
      upload_session=upload_session
    )

    order_item, created = OrderItem.objects.get_or_create(
      order=order,
      event=item['order'],
      quantity=item['quantity'],
      price=item['price'],
      final_price=item['total_price']
    )
  cart.clear()
