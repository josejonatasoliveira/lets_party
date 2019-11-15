from django.db.models import Q
from .models import UploadSession
from .models import Evento
from projeto_tg.endereco.models import Endereco
from projeto_tg.cidade.models import Cidade
from projeto_tg.base.models import TopicCategory, TopicType
from bs4 import BeautifulSoup as bs
import base64
from PIL import Image
from io import BytesIO
import uuid


def event_upload(
  image_file,
  name=None,
  user=None,
  date=None,
  title=None,
  short_description=None,
  description=None,
  category=None,
  type_event=None,
  price=None,
  street_name=None,
  number=None,
  cep=None,
  start_date=None,
  end_date=None,
  city_state=None):
  
  upload_session = UploadSession.objects.create(user=user)

  city, state = city_state.split("-")

  if city is not None and state is not None:
    city = Cidade.objects.get(name__iexact=city.strip())

  defaults_addr = {
    'street_name':street_name,
    'number':number,
    'cep':cep,
    'city':city
  }
  address, has_create = Endereco.objects.get_or_create(street_name=street_name,
                                                       number=number,
                                                       cep=cep,
                                                       city=city)
  
  if category is not None:
    categories = TopicCategory.objects.filter(Q(id__iexact=category))
    if len(categories) == 1:
      category = categories[0]
    else:
        category = None

  if type_event is not None:
    types =  TopicType.objects.filter(Q(id__iexact=type_event))
    if len(types) == 1:
      type_event = types[0]
    else:
      type_event = None

  defaults = {
        'title': title,
        'name': name,
        'short_description': short_description,
        'description': description,
        'image_file': image_file,
        'date': date,
        'upload_session': upload_session,
        'category': category,
        'type_event': type_event,
        'price': price,
        'start_date': start_date,
        'end_date': end_date,
        'address':address,
        'id_hash': str(uuid.uuid4())
    }
  
  try:
    event, created = Evento.objects.get_or_create(
                          name=name,
                          defaults=defaults
                      )
  except Exception as e:
    print(e)
    
  return event, created