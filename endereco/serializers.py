from rest_framework import serializers
from projeto_tg.cidade.serializers import CidadeSerializer
from .models import Endereco

class EnderecoSerializer(serializers.Serializer):
    street_name = serializers.CharField()
    cep = serializers.CharField()
    number = serializers.IntegerField()
    city = CidadeSerializer()
    
    def create(self, validated_data):
        return Endereco(**validated_data)
  
    def update(self, instance, validated_data):
        instance.street_name = validated_data.get('street_name', instance.street_name)
        instance.cep = validated_data.get('cep', instance.cep)
        instance.number = validated_data.get('number', instance.number)
        instance.city = validated_data.get('city', instance.city)
        
        instance.save()
        return instance