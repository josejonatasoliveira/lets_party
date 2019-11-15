from .models import Evento
from elasticsearch_dsl import DocType, Index

events = Index('events')

# @events.doc_type
class EventDocument(DocType):
    
    class Meta:
        model = Evento
        
        fields = [
            'name',
            'short_desciption',
            'description',
        ]
