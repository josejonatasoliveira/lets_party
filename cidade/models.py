from django.db import models

# Create your models here.
class Estado(models.Model):
  name = models.CharField(max_length=200)
  sigla = models.CharField(max_length=4)

  class Meta:
    db_table = 'est_estado'

class Cidade(models.Model):
    
  name = models.CharField(max_length=200)
  ibge_code = models.CharField(max_length=20)
  sigla = models.CharField(max_length=10, default="")
  estado = models.ForeignKey(Estado, default=0, on_delete=models.CASCADE)
  
  class Meta:
        db_table = 'cid_cidade'
        ordering = ['-name']
        verbose_name_plural = "Cities"


