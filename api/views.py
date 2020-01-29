from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models import Q
from django.http import Http404

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

import base64
import binascii
from Crypto.Cipher import AES

import datetime
import time

from projeto_tg.evento.serializers import EventoSerializer
from projeto_tg.cidade.serializers import CidadeSerializer, EstadoSerializer
from projeto_tg.people.serializers import ProfileSerializer, ProfileSignInSerializer
from projeto_tg.endereco.models import Endereco
from projeto_tg.evento.models import Evento, UploadSession
from projeto_tg.cidade.models import Cidade, Estado
from projeto_tg.people.models import Profile
from projeto_tg.order.models import Order, OrderItem, Ticket
from projeto_tg.order.serializers import OrderItemSerializer
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
              serializer.save()
              return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchApi(generics.ListAPIView):
      queryset = Evento.objects.all()
      serializer_class = EventoSerializer

      def get(self, request):
            q = request.GET.get('q')
            event_search = Evento.objects.filter(Q(title__icontains=q) | Q(name__icontains=q))
            results = []
            for event in event_search:
                  event.month = datetime.date(event.date.year, event.date.month, event.date.day).strftime("%b")
                  res = model_to_dict(event)
                  res['image_file'] = event.image_file.name
                  results.append(res)

            count = len(event_search)
            out = {
                  'results': results,
                  'count': count
            }

            return Response(out)

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

class ProfileSignInApi(generics.ListAPIView):
      queryset = Profile.objects.all()
      serializer_class = ProfileSignInSerializer

      def post(self, request, *args, **kwargs):
            serializer = ProfileSignInSerializer(data=request.data)

            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderApi(generics.ListAPIView):
      queryset = OrderItem.objects.all()
      serializer_class = OrderItemSerializer

      def get(self, request):
            token = request.GET.get("token")

            user = Token.objects.get(key=token).user

            orders = OrderItem.objects.filter(Q(order__upload_session__user=user))
            results = []
            for item in orders:
                  order = model_to_dict(item)
                  order['event'] = model_to_dict(item.event)
                  order['event']['image_file'] = item.event.image_file.name
                  order['event']['date'] = item.event.date.strftime("%d/%m/%Y")
                  order['address'] = model_to_dict(item.event.address)
                  order['address']['city'] = model_to_dict(item.event.address.city)
                  order['order'] = model_to_dict(item.order)
                  order['ticket'] = model_to_dict(item.ticket)
                  results.append(order)
            out = {
                  'results':results
            }

            return Response(out)

      def post(self, request, *args, **kwargs):

            token = request.data['token']

            user = Token.objects.get(key=token).user
            upload_session = UploadSession.objects.create(user=user)

            request.data['price'] = request.data['event']['price']
            request.data['final_price'] = request.data['event']['price'] * request.data['quantity']

            try:
                  order = Order.objects.create(final_value=request.data['final_price'],
                                               upload_session=upload_session)
                  event = Evento.objects.get(Q(id__exact=request.data['event']['id']))
                  try:
                        order_item, has_create = OrderItem.objects.get_or_create(
                              order=order,
                              event=event,
                              quantity= request.data['quantity'],
                              price=request.data['price'],
                              final_price=request.data['final_price']
                        )
                  except Exception as e:
                        print(e)
                  return Response(request.data, status=status.HTTP_201_CREATED)
            except:
                  return Response(request.data, status=status.HTTP_400_BAD_REQUEST)

class ProfileApi(generics.ListAPIView):
      queryset = Profile.objects.all()
      serializer_class = ProfileSerializer

      def get_objects(self, primary_key):
            try:
                  return Profile.objects.get(id__exact=primary_key)
            except Exception as e:
                  raise Http404

      def put(self, request):
            primary_key = request.POST.get("id")
            profile = self.get_objects(primary_key)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketApi(generics.ListAPIView):

      queryset = OrderItem.objects.all()
      serializer_class = OrderItemSerializer

      def unpad(self, data):
            return data[:-ord(data[-1])]

      def get(self, request):

            BLOCK_SIZE = 16
            
            encrypted_data = request.GET.get('enc_data')
            order_id = request.GET.get('id')
            authenticated = False
            
            key = OrderItem.objects.get(Q(order__id=order_id)).ticket.key.encode()
            value = OrderItem.objects.get(Q(order__id=order_id)).ticket.value
            encrypted = base64.b64decode(encrypted_data.replace(' ','+'))
            IV = encrypted[:BLOCK_SIZE]
            aes = AES.new(key, AES.MODE_CBC, IV)
            result = aes.decrypt(encrypted[BLOCK_SIZE:])

            if( value == result):
                  authenticated = True

            out = {
                  'is_authenticated': authenticated
            }

            return Response(out, status=status.HTTP_201_CREATED)
      
      def post(self, request):

            try:
                  token = request.data['token']
                  key = request.data['key']
                  order_id = request.data['order_id']
                  
                  user = Token.objects.get(key=token).user
                  order_item = OrderItem.objects.get(Q(order__id=order_id))
                  Ticket.objects.filter(id__exact=order_item.ticket.id)\
                        .update(key=key)
                  out = { 'message': 'OK' }
                  return Response(out, status=status.HTTP_201_CREATED)
            except Exception as e:
                  out = { 'message': str(e) }
                  return Response(out, status=status.HTTP_400_BAD_REQUEST)
            


