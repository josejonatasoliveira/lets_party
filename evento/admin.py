from django.contrib import admin
from projeto_tg.evento.models import Evento
# Register your models here.

class EventoAdmin(admin.ModelAdmin):

  model = Evento
  list_display = (
    'id',
    'name',
    'date',
    'short_description'
  )
  search_fields = ('name', 'date')

admin.site.register(Evento)

