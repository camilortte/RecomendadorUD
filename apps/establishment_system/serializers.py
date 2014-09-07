from apps.establishment_system.models import Categoria, SubCategoria, Establecimiento
from rest_framework import serializers


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
        fields = ('nombre','address','email','position','description','sub_categorias','web_page')



