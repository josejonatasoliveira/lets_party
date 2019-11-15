from django.conf.urls import url
from django.views.generic import TemplateView
from . import views



urlpatterns = [
    url(r'^$',
        views.index_view,
        name='event_browse'),
    url(r'^search/', views.search, name='search_event'),
    url(r'^search_for/city',views.get_cities, name="get_cities"),
    url(r'^(?P<event>[^/]*)$',views.event_detail, name="event_detail")
]