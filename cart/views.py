from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST

from projeto_tg.evento.models import Evento
from .models import Cart
from .forms import CartAddOrderItemForm


@require_POST
def cart_add(request, order_item_id):
    cart = Cart(request)
    order_item = get_object_or_404(Evento, id_hash=order_item_id)
    form = CartAddOrderItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(order_item=order_item,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, order_item_id):
    cart = Cart(request)
    order_item = get_object_or_404(Evento, id_hash=order_item_id)
    cart.remove(order_item)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddOrderItemForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    return render(request, 'cart/cart_detail.html', {'cart': cart})
