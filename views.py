from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
from projeto_tg.evento.models import Evento
from django.core.paginator import Paginator
from haystack.query import SearchQuerySet
from projeto_tg.cart.models import Cart
import json
import datetime

def index_view(request, template="index.html"):
  cart = Cart(request)
  list_events = Evento.objects.all()
  for event in list_events:
        event.month = datetime.date(event.date.year, event.date.month, event.date.day).strftime("%b")
  paginator = Paginator(list_events, 3)
  paginator_1 = Paginator(list_events, 7)

  page = request.GET.get('page')
  
  events = paginator.get_page(page)
  events_show = paginator_1.get_page(page)
  events[0].id = 0

  out = {
    'events': events,
    'events_show': events_show,
    'cart': cart
  }
  return render(request, template, out)

def get_events(request):
  list_events = Evento.objects.all()
  for event in list_events:
        event.month = datetime.date(event.date.year, event.date.month, event.date.day).strftime("%b")
  paginator = Paginator(list_events, 7)

  page = request.GET.get('page')
  
  _events = paginator.get_page(page)
  results = []

  for event in _events:
    res = model_to_dict(event)

    res['image_file'] = event.image_file.name
    res['date'] = str(event.date)
    res['start_date'] = str(event.start_date)
    res['end_date'] = str(event.end_date)

    results.append(res)

  the_data = json.dumps({
        'results': results
  })
  
  return HttpResponse(the_data, content_type='application/json')

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(text_auto=request.GET.get('q', ''))
    suggestions = [result.title for result in sqs]
    
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')

def autocomplete_city(request):
    sqs = SearchQuerySet().autocomplete(text_auto=request.GET.get('q', ''))
    suggestions = [ f"{result.title} - {result.sigla}" for result in sqs]
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
