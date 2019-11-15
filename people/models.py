from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager

from projeto_tg.endereco.models import Endereco

class ProfileUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)
    
class Profile(AbstractUser):
    
    profile = models.TextField(
        _("Profile"),
        null=True,
        blank=True
    )
    first_name = models.CharField(
        _("Primeiro nome"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("O primeiro nome do usuário")
    )
    last_name = models.CharField(
        _("Sobrenome do usuário"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Sobrenome do usuário")
    )
    phone_number = models.CharField(
        _("Número do Telefone"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Número do telefone pessoal")
    )
    cpf = models.CharField(
        _("Cpf do usuário"),
        max_length=11,
        blank=True,
        null=True,
        help_text=_("Cpf do usuário")
    )
    cnpj = models.CharField(
        _("Cnpj do usuário"),
        max_length=15,
        blank=True,
        null=True,
        help_text=_("Cnpj do usuário")
    )
    address = models.ForeignKey(Endereco,null=True, on_delete=models.SET_NULL)
    
    def get_absolute_url(self):
        return reverse("profile_detail", args=[self.username])
    
    def class_name(self, value):
        return value.__class__.__name__
    
    @property
    def name_long(self):
        if self.first_name and self.last_name:
            return '%s %s (%s)' % (self.first_name,
                                   self.last_name, self.username)
        elif (not self.first_name) and self.last_name:
            return '%s (%s)' % (self.last_name, self.username)
        elif self.first_name and (not self.last_name):
            return '%s (%s)' % (self.first_name, self.username)
        else:
            return self.username
        
    
    
    
    