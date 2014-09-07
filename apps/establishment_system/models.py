# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField
from django.utils import timezone
from imagekit.models import ImageSpecField

from imagekit.processors import ResizeToFill
from imagekit import ImageSpec
from imagekit.processors import TrimBorderColor, Adjust

from apps.account_system.models import User
from django.core import urlresolvers
from django.contrib.sites.models import Site


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

from django.contrib.contenttypes.models import ContentType
from apps.externals.djangoratings.fields import RatingField

class Establecimiento(models.Model):

    nombre= models.CharField(_('Nombre'),max_length=100,null=False,blank=False,
        help_text='Nombre legal del Establecimiento ',unique=True)
    email= models.EmailField(_('Emial'),null=True,blank=True,
        help_text='Correo electronico del Establecimiento',unique=False)
    web_page=models.URLField(_('Pagina web'),null=True,blank=True, unique=False, 
        help_text='Direccion de la pagina web ')
    address= models.CharField(_('Direccion'),max_length=100,null=False,blank=False,
        help_text='Direccion del establecimiento',unique=True)
    description=models.TextField(_('Descripcion'),null=True,blank=True,
        help_text='Una breve descripcion del establecimiento', unique=False)
    telefono= models.CharField(_('Telefono'),max_length=15,null=True,blank=True,
        help_text='Numero de telefono',unique=True)
    #longitud=models.FloatField(_('Longitud'), null=True, blank=False,help_text='Longitud')
    #latitud=models.FloatField(_('Latitud'),null=True, blank=False,help_text='Latitud')
    position = GeopositionField()
    administradores= models.ManyToManyField(User,blank=True,null=True)
    sub_categorias=models.ForeignKey(SubCategoria)
    visible = models.BooleanField(_('Is visible'), default=True,
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
    
    imagen= models.ImageField(upload_to='images_establishment', null=False, blank=False,
        help_text='Imagen perteneciente al establecimiento')
    establecimientos = models.ForeignKey(Establecimiento)
    date_uploaded = models.DateTimeField(_('date upload'), default=timezone.now)
    imagen_thumbnail = ImageSpecField(source='imagen',
                                      processors=[ ResizeToFill(125, 125),
                                                Adjust(contrast=1, sharpness=1)],
                                      format='JPEG',
                                      options={'quality': 40})
    usuarios=models.ForeignKey(User)
    class Meta:
        verbose_name = _('Imagen')
        verbose_name_plural = _('Imagenes')

    def __unicode__(self):
        return self.establecimientos.nombre


class Comentario(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    body = models.TextField(_('Ingresa tu comentario'),max_length=500, null=False, blank=False)
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


class TiposSolicitud(models.Model):

    nombre= models.CharField(_('Nombre'),max_length=100,null=False,blank=False)
    tag = models.CharField(_('Tag'),max_length=100,null=False,blank=False)
    class Meta:
        verbose_name = _('TiposSolicitud')
        verbose_name_plural = _('TiposSolicitudes')

    def __unicode__(self):
        return self.tag
    

class EstablecimientoTemporal(models.Model):
    
    nombre= models.CharField(_('Nombre'),max_length=100,null=False,blank=False,
        help_text='Nombre legal del Establecimiento ',unique=True)
    email= models.EmailField(_('Emial'),null=True,blank=True,
        help_text='Correo electronico del Establecimiento',unique=False)
    web_page=models.URLField(_('Pagina web'),null=True,blank=True, unique=False, 
        help_text='Direccion de la pagina web ')
    address= models.CharField(_('Direccion'),max_length=100,null=False,blank=False,
        help_text='Direccion del establecimiento',unique=True)
    description=models.TextField(_('Descripcion'),null=True,blank=True,
        help_text='Una breve descripcion del establecimiento', unique=False)
    position = GeopositionField()
    sub_categorias=models.ForeignKey(SubCategoria)
    #solicitudes = models.OneToOneField(Solicitud, null=True, blank=True)
    class Meta:
        verbose_name = _('Establecimiento temporal')
        verbose_name_plural = _('Establecimientos temporales')

    def __unicode__(self):
        return self.nombre    

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

"""La informacion de modificacion se guarda en establecimiento temporal"""
class Solicitud(models.Model):

    usuarios = models.ForeignKey(User)
    establecimientos= models.ForeignKey(Establecimiento)
    fecha_creada = models.DateTimeField(_('Fecha'), default=timezone.now)
    tipo_solicitudes  = models.ForeignKey(TiposSolicitud)
    contenido = models.TextField(max_length=500,null=True,blank=True)
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

    
