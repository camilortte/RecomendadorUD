# -*- encoding: utf-8 -*-

"""
    
    search_indexex.py: Creacion de los indices de busqueda.

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
#import datetime
from haystack import indexes
from .models import Establecimiento, Categoria


class EstablecimientoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nombre =  indexes.EdgeNgramField(model_attr='nombre')
    email =  indexes.EdgeNgramField(model_attr='email')
    web_page = indexes.EdgeNgramField(model_attr='web_page')
    address= indexes.EdgeNgramField(model_attr='address')    
    sub_categorias = indexes.EdgeNgramField(model_attr='sub_categorias')
#    content_auto = indexes.EdgeNgramField(model_attr='nombre')

    def get_model(self):
        return Establecimiento

    
    def index_queryset(self, using=None):
        # using select_related here should avoid an extra query for getting
        # the manufacturer when indexing
        return self.get_model().objects.all().select_related('sub_categorias')


class CategoriaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nombre_categoria= indexes.EdgeNgramField(model_attr='nombre')

    def get_model(self):
        return Categoria

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
        return self.get_model().objects.all()