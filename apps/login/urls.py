from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process_registration$', views.process_registration),
    url(r'^process_login$', views.process_login),
    url(r'^quotes$', views.quotes),
    url(r'^process_quote$', views.process_quote),
    url(r'^myaccount/(?P<id>\d+)$', views.edit),
    url(r'^process_edit$', views.process_edit),
    url(r'^process_like$', views.like),
    url(r'^delete_quote/(?P<id>\d+)$', views.delete_quote),
    url(r'^user/(?P<id>\d+)$', views.profile),
    url(r'^logout$', views.logout)
]