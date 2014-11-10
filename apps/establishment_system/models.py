# -*- encoding: utf-8 -*-

"""
    
    models.py: Modelos del sistema de establecimientos

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
import re

#Django
#from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core import urlresolvers
from django.contrib.gis.db import models 
from django.contrib.contenttypes.models import ContentType
from django.core import validators

#External apps
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import  Adjust

#Internal apps
from apps.account_system.models import User
from apps.externals.djangoratings.fields import RatingField


class Categoria(models.Model):
    """
        Modelo de categorias
    """

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
    """
        Modelo sew sub categorias
    """
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
    """
        Modelo de establecimientos
    """
    nombre= models.CharField(_('Nombre'),max_length=100,null=False,blank=False,
        help_text='Nombre legal del Establecimiento. ',unique=True,
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-><]+$'), _('Enter a valid username.'), 'invalid')
        ])
    email= models.EmailField(_('Email'),null=True,blank=True,
        help_text=u'Correo electrónico del Establecimiento',unique=False)
    web_page=models.URLField(_(u'URL Página web'),null=True,blank=True, unique=False, 
        help_text=u'Dirección URL de la página web Ej: http://www.ejemplo.com ')
    address= models.CharField(_(u'Dirección'),max_length=100,null=False,blank=False,
        help_text=u'Dirección del establecimiento ',unique=True)
    description=models.TextField(_(u'Descripción'),null=True,blank=True,
        help_text=u'Una breve descripción del establecimiento', unique=False)
    telefono= models.CharField(_(u'Teléfono'),max_length=15,null=True,blank=True,
        help_text='Numero de teléfono',unique=False)
    #longitud=models.FloatField(_('Longitud'), null=True, blank=False,help_text='Longitud')
    #latitud=models.FloatField(_('Latitud'),null=True, blank=False,help_text='Latitud')
    #position = GeopositionField()
    position =models.PointField() # GeopositionField()
    objects = models.GeoManager()
    administradores= models.ManyToManyField(User,blank=True,null=True)
    sub_categorias=models.ForeignKey(SubCategoria)
    visible = models.BooleanField(_('Es visible'), default=True,
        help_text=_('El establecimiento es visible'))
    rating = RatingField(range=5,can_change_vote = True) # 5 possible rating values, 1-5
    class Meta:
        verbose_name = _('Establecimiento')
        verbose_name_plural = _('Establecimientos')

    def __unicode__(self):
        return self.nombre


    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Imagen(models.Model):
    """
        Imagenes de los establecimientos
    """
    
    imagen= models.ImageField(upload_to='images_establishment', null=False, blank=False,
        help_text='Imagen perteneciente al establecimiento')
    establecimientos = models.ForeignKey(Establecimiento)
    date_uploaded = models.DateTimeField(_('date upload'), default=timezone.now)
    imagen_thumbnail = ImageSpecField(source='imagen',
                                      processors=[ ResizeToFill(245, 147),
                                                Adjust(contrast=1, sharpness=1)],
                                      format='JPEG',
                                      options={'quality': 80})
    usuarios=models.ForeignKey(User)
    class Meta:
        verbose_name = _('Imagen')
        verbose_name_plural = _('Imagenes')

    def __unicode__(self):
        return self.establecimientos.nombre


class Comentario(models.Model):
    """
        Modelo de comentarios
    """
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    body = models.TextField(_('Ingresa tu comentario'),max_length=500, null=False, blank=False)
    post = models.ForeignKey(Establecimiento)     
    ip_address = models.GenericIPAddressField(_('IP address'), unpack_ipv4=True, blank=True, null=True)
    is_public = models.BooleanField(_('is public'), default=True,
                    help_text=_('Si el comentario es visible '))

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))

    class Meta:
        verbose_name = _('Comentario')
        verbose_name_plural = _('Comentarios')

    

class TiposSolicitud(models.Model):
    """
        Los tipos de solicitudes para cada solicitud
    """

    nombre= models.CharField(_('Nombre'),max_length=100,null=False,blank=False)
    tag = models.CharField(_('Tag'),max_length=100,null=False,blank=False)
    class Meta:
        verbose_name = _('TiposSolicitud')
        verbose_name_plural = _('TiposSolicitudes')

    def __unicode__(self):
        return self.tag
    

class EstablecimientoTemporal(models.Model):
    """
        Representa la copia modificada de un establecimiento que se almacena 
        en una solicitud.
    """
    
    nombre= models.CharField(_('Nombre'),max_length=100,null=False,blank=False,
        help_text='Nombre legal del Establecimiento ',unique=False)
    email= models.EmailField(_('Email'),null=True,blank=True,
        help_text=u'Correo electrónico del Establecimiento',unique=False)
    web_page=models.URLField(_(u'Página web'),null=True,blank=True, unique=False, 
        help_text=u'Dirección de la página web ')
    address= models.CharField(_(u'Dirección'),max_length=100,null=False,blank=False,
        help_text=u'Dirección del establecimiento',unique=False)
    description=models.TextField(_(u'Descripción'),null=True,blank=True,
        help_text=u'Una breve descripción del establecimiento', unique=False)
    position =models.PointField() # GeopositionField()
    sub_categorias=models.ForeignKey(SubCategoria)
    objects = models.GeoManager()
    #solicitudes = models.OneToOneField(Solicitud, null=True, blank=True)
    class Meta:
        verbose_name = _('Establecimiento temporal')
        verbose_name_plural = _('Establecimientos temporales')

    def __unicode__(self):
        return self.nombre    

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Solicitud(models.Model):
    """
        Las solicitudes, dependiendo de cada solicitud las accciones serán diferentes
    """
    usuarios = models.ForeignKey(User)
    establecimientos= models.ForeignKey(Establecimiento)
    fecha_creada = models.DateTimeField(_('Fecha'), default=timezone.now)
    tipo_solicitudes  = models.ForeignKey(TiposSolicitud)
    contenido = models.TextField(_(('Descripción de la solicitud').decode('utf-8')),max_length=500,null=True,blank=True)
    establecimientos_temporales = models.ForeignKey(EstablecimientoTemporal, null=True, blank=True)    
    #establecimiento_duplicado = 
    aprobar = models.BooleanField(_('Aprobar'), default=False,
        help_text=_('Aprobar la solicitud'))
    class Meta:
        verbose_name = _('Solicitud')
        verbose_name_plural = _('Solicitudes')

    def __unicode__(self):
        #print "ESTO DEVUELVE: ",_(str(self.tipo_solicitudes)+" "+str(self.usuarios))
        #print "ESTO DEVUELVE2: ",(str(self.tipo_solicitudes)+" "+str(self.usuarios))
        return (str(self.tipo_solicitudes)+" "+str(self.usuarios)).decode('utf-8')            

    

