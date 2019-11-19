from rest_framework import serializers
from django.db.models import Q

from projeto_tg.people.models import Profile
from projeto_tg.endereco.serializers import EnderecoSerializer

class ProfileSerializer(serializers.Serializer):
  first_name = serializers.CharField()
  last_name = serializers.CharField()
  username = serializers.CharField()
  email = serializers.CharField()
  address = EnderecoSerializer()

  def update(self, instance, validated_data):
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    instance.username = validated_data.get('username', instance.username)
    instance.email = validated_data.get('email', instance.email)
    instance.address = validated_data.get('address', instance.address)


