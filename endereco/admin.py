from django.contrib import admin
from projeto_tg.endereco.models import Endereco
# Register your models here.

class EnderecoAdmin(admin.ModelAdmin):

  model = Endereco
  list_display = (
    'id',
    'street_name',
    'cep',
    'number'
  )
  search_fields = ('street_name', 'cep')

admin.site.register(Endereco)

