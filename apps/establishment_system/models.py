# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField

class Categoria(models.Model):

    nombre=models.CharField(_('Nombre categoria'),max_length=50,null=False,blank=False,unique=True,
        help_text='Nombre clave de la categoria')
    tag=models.CharField(_('Tag de la categoria'),max_length=100,null=False,blank=False, unique=False,
        help_text='Nombre que se visualiza')

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')

    def __unicode__(self):
        return self.tag
    
class SubCategoria(models.Model):
    nombre=models.CharField(_('Nombre sub-categoria'),max_length=50,null=False,blank=False,unique=True,
        help_text='Nombre clave de la sub-categoria')
    tag=models.CharField(_('Tag de la sub-categoria'),max_length=100,null=False,blank=False, unique=False,
        help_text='Nombre que se visualiza')

    categorias=models.ForeignKey(Categoria)

    class Meta:
        verbose_name = _('Sub-Categoria')
        verbose_name_plural = _('Sub-Categorias')

    def __unicode__(self):
        return self.tag


class Establecimiento(models.Model):

    nombre= models.CharField(_('Nombre'),max_length=100,null=False,blank=False,
        help_text='Nombre legal del Establecimiento ',unique=True)
    email= models.EmailField(_('Emial'),null=True,blank=True,
        help_text='Correo electronico del Establecimiento',unique=False)
    web_page=models.URLField(_('Pagina web'),null=True,blank=True, unique=False, 
        help_text='Direccion de la pagina web ')
    address= models.CharField(_('Direccion'),max_length=100,null=True,blank=True,
        help_text='Direccion del establecimiento',unique=True)
    description=models.TextField(_('Descripcion'),null=True,blank=True,
        help_text='Una breve descripcion del establecimiento', unique=False)
    #longitud=models.FloatField(_('Longitud'), null=True, blank=False,help_text='Longitud')
    #latitud=models.FloatField(_('Latitud'),null=True, blank=False,help_text='Latitud')
    position = GeopositionField()

    sub_categorias=models.ForeignKey(SubCategoria)

    class Meta:
        verbose_name = _('Establecimiento')
        verbose_name_plural = _('Establecimientos')

    def __unicode__(self):
        return self.nombre
    