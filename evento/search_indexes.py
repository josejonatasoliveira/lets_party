from haystack import indexes
from projeto_tg.evento.models import Evento
import datetime

class EventoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_auto = indexes.EdgeNgramField(model_attr='title')
    title  = indexes.CharField(model_attr='title')
    name = indexes.CharField(model_attr='name')
    image_file = indexes.CharField(model_attr="image_file")

    def get_model(self):
        return Evento