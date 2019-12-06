from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^event/', views.EventoApi.as_view(), name="api_event" ),
    url(r'^search/', views.SearchApi.as_view(), name="api_event" ),
    url(r'^get_event/', views.GetEventApi.as_view(), name="api_get_event" ),
    url(r'^state/', views.EstadoApi.as_view(), name="api_state" ),
    url(r'^city/', views.CidadeApi.as_view(), name="api_city" ),
    url(r'^profile/', views.ProfileApi.as_view(), name="api_profile" ),
    url(r'^signin/', views.ProfileSignInApi.as_view(), name="api_signin" ),
    url(r'^order/', views.OrderApi.as_view(), name="api_order" ),
    url(r'^ticket/', views.TicketApi.as_view(), name="api_ticket" ),
]