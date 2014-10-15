# -*- encoding: utf-8 -*-

"""
    
    serializers.py: Clases encargadas de serializar modelos

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

from apps.establishment_system.models import Categoria, SubCategoria, Establecimiento, Imagen
from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria

class SubCategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategoria
        fields = ('url', 'id', 'nombre', 'tag')

class ImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Imagen
        fields = ('imagen',)



class EstablecimientoSerializer(serializers.HyperlinkedModelSerializer):
    #sub_categorias = SubCategoriaSerializer('url')
    sub_categorias = serializers.PrimaryKeyRelatedField()
    imagen_set = serializers.RelatedField(many=True)
    #sub_categorias = serializers.RelatedField(source='subcategoria')
    #imagen_set = ImagenSerializer(source='imagen_thumbnail')
    class Meta:
        model=Establecimiento
        fields = (
            'id',
            'nombre',
            'address',
            'email',
            'position',
            'description',
            'sub_categorias',
            'web_page',
            'imagen_set',
            )
        depth = 1





class PaginatedEstablecimientoSerializer(PaginationSerializer):
    """
    Serializes page objects of user querysets.
    """
    class Meta:
        object_serializer_class = EstablecimientoSerializer