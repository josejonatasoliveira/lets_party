from django.db import models
from django.conf import settings
from django.utils.text import slugify
from projeto_tg.base.models import ResourceBase, ResourceBaseManager
from projeto_tg.endereco.models import Endereco
import uuid

class EventoManager(ResourceBaseManager):
  
    def __init__(self):
        models.Manager.__init__(self)

class Evento(ResourceBase):

  objects = EventoManager()
  name = models.CharField(
    help_text = "Nome pelo qual sera chamado o evento",
    null = False,
    unique = False,
    max_length=50)
  date = models.DateTimeField(
    help_text = "Data que foi criado o evento",
    null = True,
    unique = False
  )
  start_date = models.DateTimeField(
    help_text = "Data que começa o evento",
    null = True,
    unique = False
  )
  end_date = models.DateTimeField(
    help_text = "Data em que terminara o evento",
    null = True,
    unique = False
  )
  title = models.CharField(
    help_text="Titulo do evento",
    null=False,
    default="",
    max_length=40
  )
  short_description = models.CharField(
    help_text = "Pequeno resumo do evento",
    null = False,
    unique = False,
    max_length=500
  )
  description = models.TextField(
    help_text="Corpo do html com as informações do evento",
    null = False,
    default=""
  )
  image_file = models.FileField(
    help_text = "Imagem do evento",
    null = False,
    default="",
    upload_to = "events"
  )
  ticket_price = models.FloatField(
    help_text = "Preço de cada cupom",
    null = False,
    default = 0.0
  )
  price = models.DecimalField(max_digits=10, decimal_places=0, default=0.00)
  available = models.BooleanField(default=True)
  upload_session = models.ForeignKey('UploadSession', blank=True, null=True, on_delete=models.SET_NULL, default=None)
  address = models.ForeignKey(Endereco,null=True, blank=True,default=0, on_delete=models.SET_NULL)
  slug = models.SlugField(default='', blank=True)
  id_hash = models.TextField(default=str(uuid.uuid4()), unique=True)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

  class Meta:
    db_table = "eve_evento"
  
  def __str__(self):
      return self.title
    
  

class UploadSession(models.Model):

  
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    error = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)