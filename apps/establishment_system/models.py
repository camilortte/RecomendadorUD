# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

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


class Imagen(models.Model):
    
    imagen= models.ImageField(upload_to='images_establishment', null=False, blank=False,
        help_text='Imagen perteneciente al establecimiento')
    establecimientos = models.ForeignKey(Establecimiento)
    date_uploaded = date_joined = models.DateTimeField(_('date update'), default=timezone.now)
    imagen_thumbnail = ImageSpecField(source='imagen',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
    class Meta:
        verbose_name = _('Imagen')
        verbose_name_plural = _('Imagenes')

    def __unicode__(self):
        return self.establecimientos.nombre

from apps.account_system.models import User
class Comentario(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    body = models.TextField()
    post = models.ForeignKey(Establecimiento)     
    ip_address = models.GenericIPAddressField(_('IP address'), unpack_ipv4=True, blank=True, null=True)
    is_public = models.BooleanField(_('is public'), default=True,
                    help_text=_('Uncheck this box to make the comment effectively ' \
                                'disappear from the site.'))

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))

    class Meta:
        verbose_name = _('Comentario')
        verbose_name_plural = _('Comentarios')

