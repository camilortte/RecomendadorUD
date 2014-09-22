# -*- encoding: utf-8 -*-

"""
    
    urls.py: Urls del sistema de establecimientos

    @author     Camilo Ramírez
    @contact    camilolinchis@gmail.com 
                camilortte@hotmail.com
                @camilortte on Twitter
    @copyright  Copyright 2014-2015, RecomendadorUD
    @license    GPL
    @date       2014-10-10
    @satus      Pre-Alpha
    @version=   0..215


"""
from django.conf.urls import patterns, include, url
from .views import (DetalleEstablecimientoView, CommentCreateView, 
	Establecimientoslist, CrearEstablecimiento, 
	UpdateEstablecimiento,  
	Autocomplete, EliminarComentario, EstablecimientoCreateApiView, 
	CalificacionApiView, UploadImagenView, UploadImagenApiView, EstablecimientosByBoung, 
	DeleteImagen, Solicitar, EstablecimientosPropios)
from rest_framework import routers
from .api import SubCategoriaViewSet, EstablecimientoViewSet
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'sub_categoria', SubCategoriaViewSet)
router.register(r'establecimientos', EstablecimientoViewSet)


urlpatterns = patterns('',  	
	url(r'^establecimientos/(?P<pk>\d+)/upload/$', UploadImagenView.as_view(), name='establecimiento_upload_image_url'),   

	url(r'^establecimientos/(?P<pk>\d+)/$', DetalleEstablecimientoView.as_view(), name='establecimiento_detail_url'),   
	url(r'^establecimientos/$', Establecimientoslist.as_view(),		name='establecimientos_list_url'),  	 
	url(r'^establecimientos/create/$', CrearEstablecimiento.as_view(), 
			name='establecimiento_create_url'),   
	url(r'^establecimientos/update/(?P<pk>[\w-]+)$', UpdateEstablecimiento.as_view(), 
			name='establecimiento_update_url'),   
	url(r'^establecimientos/propios/',EstablecimientosPropios.as_view(),name='establecimientos_propios_ur'),
	url(r'^establecimientos/(?P<pk>\d+)/upload2/$', UploadImagenApiView.as_view(), name='establecimiento_upload_2_image_url'),
	url(r'^establecimiento/create_api/$', EstablecimientoCreateApiView.as_view(), name='user-list'),
	url(r'^establecimiento/calificar/(?P<pk>[0-9]+)/$', CalificacionApiView.as_view(), name='calificar_url'),	
	url(r'^establecimiento/boung/$', EstablecimientosByBoung.as_view(), name='establecimientos_by_boung_url'),	
	url(r'^imagen/delete/(?P<pk>\d+)/(?P<est_id>\d+)/$', 
			DeleteImagen.as_view(), name='eliminar_imagen_url'), 
	
	url(r'^comments/delete/(?P<establecimiento_id>\d+)/(?P<comentario_id>\d+)/$', 
			EliminarComentario.as_view(), name='eliminar_comentario_url'),  
	url( r'^comments/post/(?P<pk>\d+)$', CommentCreateView.as_view(),name='crear_comentario_url' ),

	url(r'^search/', include('haystack.urls')),	
	url(r'^buscar_json/$', Autocomplete.as_view(), name='auto_json'),

	url(r'^api2/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),	

	url(r'^solicitud/(?P<tipo_solicitud>\d+)/(?P<establecimiento_id>\d)/$',Solicitar.as_view(),name='solicitud_url'),
	
	#url(r'^buscar/$', Busqueda.as_view(), name='buscar_url'), 
	#url(r'^establecimiento/create_api/$', EstablecimientoCreateApiView.as_view(model=Establecimiento), name='user-list')
	#url(r'^establecimientos/create2/$', CrearEstablecimiento2.as_view()),
	#url(r'^selectable/', include('selectable.urls')),	


)

