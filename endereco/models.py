from django.db import models
from projeto_tg.cidade.models import Cidade

# Create your models here.

class Endereco(models.Model):

  street_name = models.CharField(
    help_text = "Nome de Rua, Avenida, Rodovia",
    null = False,
    unique = False,
    max_length=200)
  cep = models.CharField(
    help_text = "Cep da Rua, Avenida, Rodovia",
    null = False,
    unique = False,
    max_length=12)
  number = models.IntegerField(
    help_text = "Numero da Rua, Avenida, Rodovia",
    null = False,
    unique = False)
  city = models.ForeignKey(Cidade, default=0, on_delete=models.CASCADE)

  class Meta:
    db_table = 'end_endereco'