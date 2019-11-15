from django.contrib import admin
from projeto_tg.cidade.models import Cidade, Estado
# Register your models here.

class CidadeAdmin(admin.ModelAdmin):

  model = Cidade
  list_display = (
    'id',
    'name',
    'sigla',
    'ibge_code'
  )
  search_fields = ('name', 'sigla')

admin.site.register(Cidade)

class EstadoAdmin(admin.ModelAdmin):
    
  model = Estado
  list_display = (
    'id',
    'name',
    'sigla'
  )
  search_fields = ('name', 'sigla')

admin.site.register(Estado)