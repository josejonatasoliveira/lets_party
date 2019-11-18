"""projeto_tg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib.auth import views
from . import views as index_view

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"^account/", include("allauth.urls")),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^api/v1/", include("projeto_tg.api.urls")),
    url(r"^api/v1/auth/", include("djoser.urls.authtoken")),
    url(r'^social-auth/', include('social_django.urls', namespace="social")),
    # path('accounts/', include('django.contrib.auth.urls')),
    url(r'^$',index_view.index_view,name='home'),
    url(r'^cart/', include(('projeto_tg.cart.urls', 'cart'), namespace='cart')),
    url(r'event_carousel/',index_view.get_events),
    url(r'^event/', include('projeto_tg.evento.urls')),
    url(r'^profile/', include('projeto_tg.people.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^search/autocomplete_city', index_view.autocomplete_city),
    url(r'^search/autocomplete', index_view.autocomplete)

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.LOCAL_MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
