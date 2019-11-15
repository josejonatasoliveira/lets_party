from django.contrib import admin
from projeto_tg.order.models import Order

class OrderAdmin(admin.ModelAdmin):
  model = Order
  list_display = [
    'timestamp',
    'value',
    'discount',
    'final_value',
    'is_paid' 
  ]

admin.site.register(Order)
