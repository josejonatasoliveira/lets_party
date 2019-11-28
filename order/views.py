from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect

from .utils import checkout_order
from projeto_tg.cart.models import Cart
from .models import OrderItem
# Create your views here.

def add_order(request, template='order/order_list.html'):

  cart = Cart(request)

  if request.method == 'POST':
    checkout_order(
      cart = cart,
      user = request.user
    )
    orders = OrderItem.objects.filter(Q(order__upload_session__user=request.user))
    out = {
      'order_itens':orders
    }
    return HttpResponseRedirect('/order/')
  if request.method == 'GET':
    orders = OrderItem.objects.filter(Q(order__upload_session__user=request.user))
    out = {
      'order_itens':orders
    }
    return render(request, template, out)
