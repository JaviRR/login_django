from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process_registration$', views.process_registration),
    url(r'^process_login$', views.process_login),
    url(r'^success$', views.success)
]