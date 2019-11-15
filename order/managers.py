from django.db import models

class OrderManager(models.Manager):

  def active(self):
    return self.filter(active=True)
