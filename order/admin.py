from django.contrib import admin
from projeto_tg.order.models import Order, OrderItem, Ticket

class OrderAdmin(admin.ModelAdmin):
  model = Order
  list_display = [
    'timestamp',
    'value',
    'discount',
    'final_value',
    'is_paid' 
  ]

class OrderItemAdmin(admin.ModelAdmin):
  model = OrderItem
  list_display = [
    'order',
    'event',
    'ticket',
    'quantity',
    'price',
    'final_price'
  ]

class TicketAdmin(admin.ModelAdmin):
  model = Ticket
  list_display = [
    'key',
    'is_active',
    'created_at',
    'update_at'
  ]

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Ticket)
