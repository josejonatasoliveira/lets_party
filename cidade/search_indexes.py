from haystack import indexes
from projeto_tg.cidade.models import Cidade
import datetime

class CidadeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_auto = indexes.EdgeNgramField(model_attr='name')
    title = indexes.CharField(model_attr='name')
    sigla = indexes.CharField(model_attr='sigla')

    def get_model(self):
        return Cidade
    
    # def index_queryset(self, using=None):
    #     return self.get_model().objects.all()