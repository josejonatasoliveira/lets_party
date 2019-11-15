from django.db import models
from polymorphic.models import PolymorphicModel, PolymorphicManager
from taggit.models import TagBase, ItemBase
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q, signals

# Create your models here.

class TopicCategory(models.Model):

  identifier = models.CharField(max_length=255, default="")
  slug = models.SlugField(max_length=50, unique=True, default="")
  description = models.TextField(default="")
  fa_class = models.CharField(max_length=64, default="fa-times")
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  
  class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Categories"

  

class TopicType(models.Model):

  identifier = models.CharField(max_length=255, default="Público")
  description = models.TextField(default="")
  fa_class = models.CharField(max_length=64, default="fa-times")
  is_active = models.BooleanField(default=True) 
  created_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  
  class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Types"

class ResourceBase(PolymorphicModel, ItemBase):
  
  category_help_text = _("Categoria a qual o evento se encaixa")
  type_help_text = _("Tipo do evento")
  
  category = models.ForeignKey(
    TopicCategory,
    null=True,
    blank=True,
    help_text=category_help_text,
    on_delete=models.SET_NULL)
    
  type_event = models.ForeignKey(
    TopicType,
    null=True,
    blank=True,
    help_text=type_help_text,
    on_delete=models.SET_NULL)

class ResourceBaseManager(PolymorphicManager):
    def admin_contact(self):
        # this assumes there is at least one superuser
        superusers = get_user_model().objects.filter(is_superuser=True).order_by('id')
        if superusers.count() == 0:
            raise RuntimeError(
                'GeoNode needs at least one admin/superuser set')

        return superusers[0]

    def get_queryset(self):
        return super(
            ResourceBaseManager,
            self).get_queryset().non_polymorphic()


