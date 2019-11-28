from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q

from projeto_tg.people.models import Profile
from projeto_tg.endereco.models import Endereco
from projeto_tg.cidade.models import Estado
from projeto_tg.cidade.models import Cidade
from projeto_tg.endereco.serializers import EnderecoSerializer

UserModel = get_user_model()

class ProfileSignInSerializer(serializers.Serializer):
  username = serializers.CharField(write_only=True)
  email = serializers.CharField(write_only=True)
  password = serializers.CharField(write_only=True)

  def create(self, validated_data):
    user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
    user.set_password(validated_data['password'])
    user.save()
    return user

  def update(self, instance, validated_data):
    instance.username = validated_data.get('username', instance.username)
    instance.email = validated_data.get('email', instance.email)
    instance.password = validated_data.get('password', instance.password)

class ProfileSerializer(serializers.Serializer):
  id = serializers.IntegerField()
  first_name = serializers.CharField()
  last_name = serializers.CharField()
  username = serializers.CharField()
  email = serializers.CharField()
  address = EnderecoSerializer()

  def create(self, validated_data):
    address = validated_data['address']
    city = address['city']
    state = city['estado']

    state = Estado.objects.get(Q(name__iexact=state['name'], sigla__iexact=state['sigla']))

    city['estado'] = state
    city = Cidade.objects.get(Q(name__iexact=city['name'], sigla__iexact=city['sigla']))

    address['city'] = city

    try:
      adrr = Endereco.objects.get(Q(street_name__exact=address['street_name'], number__exact=address['number']))
    except:
      adrr = Endereco.objects.create(**address)

    validated_data['address'] = adrr
    breakpoint()

    Profile.objects.filter(Q(id__exact=validated_data['id'])).update(**validated_data)

    return Profile(**validated_data)

  def update(self, instance, validated_data):
    instance.id = validated_data.get('id', instance.id)
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    instance.username = validated_data.get('username', instance.username)
    instance.email = validated_data.get('email', instance.email)
    instance.address = validated_data.get('address', instance.address)


