from django.shortcuts import render
from django.conf import settings
from decimal import Decimal
from projeto_tg.evento.models import Evento
from django.db import models

# Create your views here.

class Cart(object):

  def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

  def add(self, order_item, quantity=1, update_quantity=False):
    order_item_id = order_item.id_hash
    if order_item_id not in self.cart:
      self.cart[order_item_id] = {
                            'quantity': 0,
                            'price':str(order_item.price)}
    if update_quantity:
      self.cart[order_item_id]['quantity'] = quantity
    else:
      self.cart[order_item_id]['quantity'] += quantity
    self.save()

  def save(self):
    self.session[settings.CART_SESSION_ID] = self.cart
    self.session.modified = True

  def remove(self, order_item):
    order_item_id = order_item.id_hash
    if order_item_id in self.cart:
      del self.cart[order_item_id]
      self.save()
  
  def __iter__(self):
    order_item_ids = self.cart.keys()
    orders = Evento.objects.filter(id_hash__in=order_item_ids)
    for order in orders:
      self.cart[str(order.id_hash)]['order'] = order
    
    for item in self.cart.values():
      item['price'] = Decimal(item['price'])
      item['total_price'] = item['price'] * item['quantity']
      yield item

  def __len__(self):
    return sum(item['quantity'] for item in self.cart.values())

  def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

  def clear(self):
      # remove cart from session
      del self.session[settings.CART_SESSION_ID]
      self.session.modified = True
