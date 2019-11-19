from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models import Q

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from projeto_tg.evento.serializers import EventoSerializer
from projeto_tg.cidade.serializers import CidadeSerializer, EstadoSerializer
from projeto_tg.endereco.models import Endereco
from projeto_tg.evento.models import Evento, UploadSession
from projeto_tg.cidade.models import Cidade, Estado
from projeto_tg.people.models import Profile
from projeto_tg.api.pagination_cfg import EventPagination, StatePagination, CityPagination

import json

class EventoApi(generics.ListAPIView):
  
  queryset = Evento.objects.all()
  serializer_class = EventoSerializer
  pagination_class = EventPagination
  
  def post(self, request):
        permission_classes = [IsAuthenticated]
        upload_session = UploadSession.objects.create(user=request.user)
        request.data['upload_session'] = upload_session
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
              breakpoint()
              serializer.save()
              return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetEventApi(generics.ListAPIView):
      queryset = Evento.objects.all()
      serializer_class = EventoSerializer
      
      def get(self, request):
            id_hash = request.GET.get("id_hash")
            data = {}
            try:
                  event = Evento.objects.get(Q(id_hash__exact=id_hash))
                  data = model_to_dict(event)
                  data['image_file'] = event.image_file.name
                  data['address'] = model_to_dict(event.address)
                  data['category'] = model_to_dict(event.category)
                  data['event_type'] = model_to_dict(event.type_event)
                  data['address']['city'] = model_to_dict(event.address.city)
                  data['address']['city']['estado'] = model_to_dict(event.address.city.estado)
                  
            except Exception as e:
                  data['result'] = 'Evento não encontrado!'
                  data['error'] = str(e)
            
            return Response(data, status=status.HTTP_201_CREATED)
      
class EstadoApi(generics.ListAPIView):
      queryset = Estado.objects.distinct('name', 'sigla')
      serializer_class = EstadoSerializer
      pagination_class = StatePagination

class CidadeApi(generics.ListAPIView):
      queryset = Cidade.objects.all()
      serializer_class = CidadeSerializer
      pagination_class = CityPagination

class ProfileApi(generics.ListAPIView):
      queryset = Profile.objects.all()

