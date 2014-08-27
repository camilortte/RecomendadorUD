from tastypie.resources import ModelResource
from .models import Establecimiento, SubCategoria, Categoria
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie import fields, utils

class EstablecimientoResource(ModelResource):
    class Meta:
        queryset = Establecimiento.objects.all()
        resource_name = 'Establecimiento'
        limit = 0
        include_resource_uri = False
        filtering = {
            'id' : ALL,
        }

    def alter_list_data_to_serialize(self, request,data):
    	#print "ENTRO ALERT LISTS ", data['id']
        return data['objects']
 
    def dehydrate_id(self, bundle):
        return int(bundle.data['id'])

#SubCategoria.objects.filter(categorias=Categoria.objects.filter(id=1))



class CategoriaResource(ModelResource):
    class Meta:
        queryset = Categoria.objects.all()
        resource_name = 'CategoriaResource'
        fields=['']
        excludes=['categorias']
        include_resource_uri = False



class SubCategoriaResource(ModelResource):

    #categorias= fields.ToManyField('apps.establishmet_system.api.SubCategoriaResource','categorias',  full=True)
    categorias = fields.ForeignKey(CategoriaResource, 'categorias',full=True)
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        }
    class Meta:
        queryset = SubCategoria.objects.all()
        resource_name = 'SubCategoriaResource'
        include_resource_uri = False
        filtering = {
            'categorias' :ALL_WITH_RELATIONS,
        }
        fields = ['id','tag']
        excludes=['categorias',]

    def alter_list_data_to_serialize(self, request,data):
        #print "ENTRO ALERT LISTS ", data['id']
        return data['objects']

    def obj_create(self, bundle, request, **kwargs):
        return super(SubCategoriaResource, self).obj_create(bundle, request, author=request.user)



from django.conf.urls import url, patterns, include
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = Establecimiento



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)