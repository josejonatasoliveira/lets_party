from django.db import models
from .managers import OrderManager
from projeto_tg.evento.models import Evento
from datetime import datetime

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

  class Meta:
    db_table = 'ord_order'

class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  event = models.ForeignKey(Evento, on_delete=models.PROTECT, default=22, null=True)
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
        



