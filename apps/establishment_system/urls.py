# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import detalle_establecimiento, CommentCreateView, Establecimientoslist, CrearEstablecimiento, UpdateEstablecimiento
from .api import EstablecimientoResource, SubCategoriaResource

entry_resource = SubCategoriaResource()


from rest_framework import routers
from .views import GroupViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)


urlpatterns = patterns('',  
	url( r'^comments/post/(?P<pk>\d+)$', CommentCreateView.as_view(),name='crear_comentario_url' ),

	url(r'^establecimientos/(?P<pk>\d+)/$', detalle_establecimiento.as_view(), 
		name='establecimiento_detail_url'),   
	url(r'^establecimientos/$', Establecimientoslist.as_view(), 
		name='establecimientos_list_url'),   
	url(r'^comments/delete/(?P<establecimiento_id>\d+)/(?P<comentario_id>\d+)/$', 
		'apps.establishment_system.views.eliminar_comentario', name='eliminar_comentario_url'),   
	url(r'^establecimientos/create/$', CrearEstablecimiento.as_view(), 
		name='establecimiento_create_url'),   
	url(r'^establecimientos/update/(?P<pk>[\w-]+)$', UpdateEstablecimiento.as_view(), 
		name='establecimiento_update_url'),   

	(r'^api/', include(entry_resource.urls)),
	url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^snippets/$', 'apps.establishment_system.views.snippet_list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', 'apps.establishment_system.views.snippet_list'),

)

