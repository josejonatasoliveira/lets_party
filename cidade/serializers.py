from rest_framework import serializers
from projeto_tg.cidade.models import Cidade

class EstadoSerializer(serializers.Serializer):
    name = serializers.CharField()
    sigla = serializers.CharField()
    
class CidadeSerializer(serializers.Serializer):
    name = serializers.CharField()
    ibge_code = serializers.CharField()
    sigla = serializers.CharField()
    estado = EstadoSerializer()
    
    def create(self, validated_data):
        return Cidade(**validated_data)
    