from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls import include, patterns, url


    
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/instagram/$', views.instagram, name='instagram'),
    url(r'^post/bestfit/$', views.bestfit, name='bestfit'),
    url(r'^post/parser/$', views.parser, name='parser'),
]