from django import forms
from projeto_tg.endereco.models import Endereco


class EnderecoForm(forms.ModelForm):
    
    class Meta:
        model = Endereco
        fields = ('street_name',
                  'cep',
                  'number'
                  )