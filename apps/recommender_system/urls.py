# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import RecomendacionView

urlpatterns = patterns('',  	
	url(r'^recomendacion/$', RecomendacionView.as_view(), name='recmendacion_url'),
)

