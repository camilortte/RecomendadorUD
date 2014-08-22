# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import detalle_establecimiento

urlpatterns = patterns('',  
	url(r'^blog/comments/', include('fluent_comments.urls')),
	url(r'^establecimiento/(?P<pk>\d+)/$', detalle_establecimiento.as_view(), 
		name='establecimiento_detail_url'),  
)

