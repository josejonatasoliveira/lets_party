from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .forms import DocumentForm
from .utils import event_upload

import json
from projeto_tg.evento.models import Evento
from projeto_tg.cidade.models import Cidade
from projeto_tg.cidade.models import Estado
from projeto_tg.cart.models import Cart
from projeto_tg.cart.forms import CartAddOrderItemForm

from projeto_tg.base.models import TopicCategory, TopicType
from .documents import EventDocument
from projeto_tg.endereco.forms import EnderecoForm
import datetime
import logging

logger = logging.getLogger(__name__)

@login_required
def index_view(request, template="evento_add.html"):
  cart = Cart(request)
  logger.error('Something went wrong!')
  if request.method == 'POST':
    form_address = EnderecoForm(request.POST)
    form = DocumentForm(request.POST, request.FILES)
    breakpoint()
    if form.is_valid():
      evento_saved, has_creat = event_upload(
          form.cleaned_data['image_file'],
          form.cleaned_data['name'],
          request.user,
          form.cleaned_data['date'],
          form.cleaned_data['title'],
          form.cleaned_data['short_description'],
          form.cleaned_data['description'],
          request.POST['category'],
          request.POST['type_event'],
          request.POST['price'],
          request.POST['street_name'],
          request.POST['number'],
          request.POST['cep'],
          form.cleaned_data['start_date'],
          form.cleaned_data['end_date'],
          request.POST['city']
      )
      return render(request, "evento_detail.html", {'event':evento_saved, 'cart': cart})
    return render(request, "evento_add.html")
  else:
    form = EnderecoForm()

    list_categories = TopicCategory.objects.all()
    list_types = TopicType.objects.all()
    list_state = Estado.objects.distinct('name','sigla')

    out = {
      'form': form,
      'categories': list_categories,
      'types': list_types,
      'list_state':list_state,
      'cart': cart
    }
    
    return render(request, template, out)


def get_events_carousel(request):
  event_list = Evento.objects.all()
  try:
    context = {
      'events' : event_list
    }
  except Exception as e:
    context = {
      'error': e
    }
  return HttpResponse(context, content_type='application/json')


def event_detail(request, event, template="evento_detail.html"):
  cart = Cart(request)
  event = Evento.objects.filter(id_hash__exact=event)
  out = {
    'event': event[0],
    'cart': cart
  }

  return render(request, template, out)

def search(request, template="evento_list.html"):
  cart = Cart(request)
  q = request.GET.get('q')
  event_search = Evento.objects.filter(Q(title__icontains=q) | Q(name__icontains=q))
  for event in event_search:
        event.month = datetime.date(event.date.year, event.date.month, event.date.day).strftime("%b")
  count = len(event_search)
  return render(request, template, {'event_search':event_search,'count':count, 'cart': cart})


def get_cities(request, template="evento_detail.html"):
    sigla = request.GET.get('sigla')
    list_city = Cidade.objects.filter(sigla__exact=sigla).order_by('name')
    cities = [x.name for x in list_city]
    cart_event_form = CartAddOrderItemForm()
    
    the_data = json.dumps({
        'results': cities,
        'cart_event_form': cart_event_form
    })
    return HttpResponse(the_data, content_type='application/json')
  
