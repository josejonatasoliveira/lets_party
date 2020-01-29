from django.db import models
from django.conf import settings
from .managers import OrderManager
from projeto_tg.evento.models import Evento, UploadSession
from datetime import datetime
import uuid

class Order(models.Model):
  timestamp = models.DateTimeField(default=datetime.now())
  value = models.DecimalField(
    help_text="Preço de cada ticket",
    decimal_places=2,
    default=0.00,
    max_digits=20
  )
  discount = models.DecimalField(
    help_text="Desconto sobre o ticket se houver",
    decimal_places=2,
    default=0.00,
    max_digits=20
  )
  final_value = models.DecimalField(
    help_text="Valor final do ticket já com o desconto",
    decimal_places=2,
    default=0.00,
    max_digits=20
  )
  is_paid = models.BooleanField(
    help_text="Se a ordem foi paga ou não",
    default=True
  )
  upload_session = models.ForeignKey(UploadSession, blank=True, null=True, on_delete=models.SET_NULL, default=None)

  class Meta:
    db_table = 'ord_order'


class Ticket(models.Model):

  key = models.CharField(
    help_text="Chave atualizado do ticket",
    max_length=16,
    default=uuid.uuid1().hex[:16],
    unique=True
  )
  value = models.CharField(max_length=255, default="")
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)

  class Meta: 
    db_table = "tic_ticket"

class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  event = models.ForeignKey(Evento, on_delete=models.PROTECT, default=22, null=True)
  ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, null=True)
  quantity = models.IntegerField(default=1) 
  price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
  final_price = models.DecimalField(default=0.0,decimal_places=2, max_digits=20)

  class Meta:
    db_table = "order_event"
    
  def total(self):
        return self.quantity * self.order.final_value
      
  def augment_quantity(self, quantity):
        self.quantity += int(quantity)
        self.save()

