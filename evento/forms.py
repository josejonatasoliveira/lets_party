from django import forms
from projeto_tg.evento.models import Evento


class DocumentForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        fields = ('name',
                  'title',
                  'short_description',
                  'description',
                  'date', 
                  'image_file',
                  'start_date',
                  'end_date',
                  'price'
                  )