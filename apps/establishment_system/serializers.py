from apps.establishment_system.models import Categoria, SubCategoria, Establecimiento
from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria

class SubCategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategoria
        fields = ('url', 'id', 'nombre', 'tag')


class EstablecimientoSerializer(serializers.HyperlinkedModelSerializer):
    #sub_categorias = SubCategoriaSerializer('url')
    sub_categorias = serializers.PrimaryKeyRelatedField()
    #sub_categorias = serializers.RelatedField(source='subcategoria')
    class Meta:
        model=Establecimiento
        fields = ('id','nombre','address','email','position','description','sub_categorias','web_page')



class PaginatedEstablecimientoSerializer(PaginationSerializer):
    """
    Serializes page objects of user querysets.
    """
    class Meta:
        object_serializer_class = EstablecimientoSerializer