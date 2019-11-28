from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q

from projeto_tg.endereco.serializers import EnderecoSerializer
from projeto_tg.base.serializers import TopicCategorySerializer, TopicTypeSerializer
from projeto_tg.endereco.models import Endereco
from projeto_tg.cidade.models import Cidade, Estado

from .models import Evento, UploadSession

class UserSerializer(serializers.Serializer):
      username = serializers.CharField()
      
      def create(self, validated_data):
            return User(**validated_data)

class UploadSessionSerializer(serializers.Serializer):
      date = serializers.DateTimeField()
      user = UserSerializer()
      processed = serializers.CharField()
      error = serializers.CharField()
      traceback = serializers.CharField()
      context = serializers.CharField()
      
      def create(self, validated_data):
            return UploadSession(**validated_data)

class EventoSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  id_hash = serializers.CharField(read_only=True)
  name = serializers.CharField()
  title = serializers.CharField()
  date = serializers.DateTimeField(format="%d-%m-%Y")
  start_date = serializers.DateTimeField()
  end_date = serializers.DateTimeField()
  description = serializers.CharField()
  short_description = serializers.CharField()
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  image_file = serializers.CharField()
  address = EnderecoSerializer()
  category = TopicCategorySerializer(read_only=True)
  type_event = TopicTypeSerializer(read_only=True)
  upload_session = UploadSessionSerializer()

  def create(self, validated_data):
    address = validated_data['address']
    city = address['city']
    state = city['estado']
    
    state = Estado.objects.get(Q(name__exact=state['name'], sigla__exact=state['sigla']))

    city['estado'] = state
    city = Cidade.objects.get(Q(name__exact=city['name'], sigla__exact=city['sigla']))
    
    address['city'] = city

    try:
      adrr = Endereco.objects.filter(Q(street_name__exact=address['street_name']))
    except:
      adrr = Endereco.objects.create(**address)
    
    validated_data['address'] = adrr
    Evento.objects.create(**validated_data)
    
    return Evento(**validated_data)
  
  def update(self, instance, validated_data):
    instance.id = validated_data.get('id', instance.id)
    instance.id_hash = validated_data.get('id_hash', instance.id_hash)
    instance.name = validated_data.get('name', instance.name)
    instance.title = validated_data.get('title', instance.title)
    instance.date = validated_data.get('date', instance.date)
    instance.start_date = validated_data.get('start_date', instance.start_date)
    instance.end_date = validated_data.get('end_date', instance.end_date)
    instance.description = validated_data.get('description', instance.description)
    instance.short_description = validated_data.get('short_description', instance.short_description)
    instance.price = validated_data.get('price', instance.price)
    instance.image_file = validated_data.get('image_file', instance.image_file)
    instance.address = validated_data.get('address', instance.address)
    instance.category = validated_data.get('category', instance.category)
    instance.upload_session = validated_data.get('upload_session', instance.upload_session)
    
    instance.save()
    return instance