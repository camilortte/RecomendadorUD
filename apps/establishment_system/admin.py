# -*- encoding: utf-8 -*-
"""
    
    admin: modelos de administración del systema de establecimientos

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
from datetime import datetime

#Django
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages, admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError

#External apps
from notifications import notify

#Models
from .models import (
    Categoria, Establecimiento, 
    SubCategoria, Imagen ,EstablecimientoTemporal, 
    Solicitud, TiposSolicitud,Comentario)

#Forms
from .forms import EstablecimientoAdminForm


class CommentAdmin(admin.ModelAdmin):
    u"""
        Clase encargada de presentar los comentarios en el admin
    """
    # raw_id_fields = ('post', )
    # list_display= ('author', 'post', 'body', 'is_public',)
    # list_filter = ('is_public',)
    # search_fields = ('post', )
    # ordering = ('author',)

    class Meta:
        model = Comentario


class ImagenInline(admin.StackedInline):
    """
        Clase encargada de presentar las imagenes inline en el modelo del establecimiento.
    """
    model = Imagen


class SolicitudAdmin(admin.ModelAdmin):
    u"""
        Clase encargada de presentar las solicitudes en el admin
    """

    list_display = ('usuarios','establecimientos','tipo_solicitudes','aprobar')    
    change_form_template = 'establishment/admin.html'
    fieldsets = (
        (None, {
            'fields': ('usuarios','tipo_solicitudes',  'establecimientos', 'contenido' ,'establecimientos_temporales')
        }),
        ('Advanced options', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('fecha_creada','aprobar')
        }),
    )
    list_filter = ('tipo_solicitudes','aprobar',)
    search_fields = ('usuarios', 'establecimientos', )
    ordering = ('fecha_creada',)


    def change_view(self, request, object_id, form_url='', extra_context=None): 
        """
            Se agregan al contexto los ddatos de la solicitud
        """
        extra_context = extra_context or {}     

        try:
            obj=Solicitud.objects.get(id=object_id)
            id_establecimiento=obj.establecimientos.id
        except Exception:
            id_establecimiento=False
        
        try:
            id_establecimiento_temporal = obj.establecimientos_temporales.id
        except Exception:
            id_establecimiento_temporal =False

      
        #Query de establecimiento
        if id_establecimiento:
            for establecimiento in  Establecimiento.objects.filter(id=id_establecimiento):
                establecimiento.fields = dict((field.name, field.value_to_string(establecimiento))
                                                    for field in establecimiento._meta.fields)

        else:
            establecimiento=False

        #Query de establecimiento temporal
        if id_establecimiento_temporal:
            for establecimiento_temporal in  EstablecimientoTemporal.objects.filter(id=id_establecimiento_temporal):
                establecimiento_temporal.fields = dict((field.name, field.value_to_string(establecimiento_temporal))
                                                    for field in establecimiento_temporal._meta.fields)
        else:
            establecimiento_temporal=False

        if establecimiento:
            extra_context['establecimiento'] = establecimiento        
        if establecimiento_temporal:
            extra_context['establecimiento_temporal'] = establecimiento_temporal
        return super(SolicitudAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    class Media:
        js = (    
            'http://code.jquery.com/jquery-2.1.1.min.js', # jquery
            'js/related_solicitud_admin.js',       # project static folder
        )

    class Meta:
        model = Solicitud
    
    
    def get_readonly_fields(self, request, obj=None):  
        """
            Si la solicitud se aprobo ya no puede editarse
        """
        if obj is not None :
            if obj.aprobar:
                return self.fields or [f.name for f in self.model._meta.fields]        
        return super(SolicitudAdmin, self).get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        """
            Almacena la solicitud dependiendo tel tipo de solicitud al que 
            corresponde
        """
        print obj.aprobar
        if  obj.aprobar:
            try:
                if form.cleaned_data['aprobar'] == True:
                    if form.cleaned_data['tipo_solicitudes'].nombre=='eliminacion':         
                        if self.aprobar_eliminacion(request,form,obj):
                            obj.save()
                            saludo=u"Hola "+ obj.usuarios.first_name+", tu Solicitud de "\
                            +form.cleaned_data['tipo_solicitudes'].tag+" fue aprobada.".decode('utf-8')
                            notify.send(
                                        request.user,
                                        recipient= obj.usuarios,
                                        verb="Solicitud aprobada",                    
                                        description=saludo,
                                        timestamp=datetime.now()
                                    ) 
                            print "Solicitud de aliminacion Aprobada"
                    elif form.cleaned_data['tipo_solicitudes'].nombre=='modificacion':
                        if self.aprobar_modificacion(request,form,obj):      
                            obj.save()
                            saludo=u"Hola "+ obj.usuarios.first_name+", tu Solicitud de "\
                            +form.cleaned_data['tipo_solicitudes'].tag+" fue aprobada.".decode('utf-8')
                            notify.send(
                                        request.user,
                                        recipient= obj.usuarios,
                                        verb="Solicitud aprobada",                    
                                        description=saludo,
                                        timestamp=datetime.now()
                                    ) 
                            print "Solicitud de modificacion Aprobada"
                    elif form.cleaned_data['tipo_solicitudes'].nombre=='administracion':
                        if self.aprobar_administracion(request,form,obj):                            
                            obj.save()
                            saludo=u"Hola "+ obj.usuarios.first_name+", tu Solicitud de "\
                            +form.cleaned_data['tipo_solicitudes'].tag+" fue aprobada.".decode('utf-8')
                            notify.send(
                                        request.user,
                                        recipient= obj.usuarios,
                                        verb="Solicitud aprobada",                    
                                        description=saludo,
                                        timestamp=datetime.now()
                                    ) 
                            print "Solicitud de administracion Aprobada"
                    elif form.cleaned_data['tipo_solicitudes'].nombre=='desactivacion':
                        if self.aprobar_desactivacon(request,form,obj):                  
                            obj.save()
                            saludo=u"Hola "+ obj.usuarios.first_name+", tu Solicitud de "\
                            +form.cleaned_data['tipo_solicitudes'].tag+" fue aprobada.".decode('utf-8')
                            notify.send(
                                        request.user,
                                        recipient= obj.usuarios,
                                        verb="Solicitud aprobada",                    
                                        description=saludo,
                                        timestamp=datetime.now()
                                    ) 
                            print "Solicitud de desactivacion Aprobada"

            except Exception, e:                                
                print "No se puede editar: ",e     
                #raise e      
            
        else:
            obj.save()

    def aprobar_desactivacon(self,request,form,obj):           
        """
            Aprueba desactivar un establecimeinto
        """
        try:
            obj.establecimientos.visible=False
            obj.establecimientos.save()               
            self.message_user(request,
                            _(("Se aprobó la desactivacion de eliminacion del establecimiento"+str(obj.establecimientos)).decode("utf-8")),
                             level=messages.INFO, extra_tags='', fail_silently=False)            
            return True
        except Exception, e:
            print "ERROR: ", e
            self.message_user(request,
                            _(("No Se aprobó la solicitud de eliminacion del establecimiento"+str(obj.establecimientos)).decode("utf-8")),
                             level=messages.ERROR, extra_tags='', fail_silently=False)
            return False
        


    #Metodo cuando se aprueba una solicitud de elmiminacion
    def aprobar_eliminacion(self,request,form,obj):
        """
            Aprueba eliminar un establecimiento
        """
        try:
            object_id=str(obj.id)
            ###ELIMINACION DE ESTABLECIMIENTO
            obj.establecimientos.delete()
            ###ELIMINACION DE ESTABLECIMIENTO
            super(SolicitudAdmin, self).delete_view(request, object_id, extra_context=None)        
            self.message_user(request,
                            _(("Se aprobó la solicitud de eliminacion del establecimiento"+str(obj.establecimientos)).decode("utf-8")),
                             level=messages.INFO, extra_tags='', fail_silently=False)
            return True
        except Exception, e:            
            print "ERROR: ", e
            self.message_user(request,
                            _(("No Se aprobó la solicitud de eliminacion del establecimiento"+str(obj.establecimientos)).decode("utf-8")),
                             level=messages.ERROR, extra_tags='', fail_silently=False)
            return False
        
    
    #Metodo cuando se aprueba solicitud de modificacion
    def aprobar_modificacion(self,request,form,obj):
        """
            Aprueba modificar un establecimiento
        """
        #establecimientos_temporales=EstablecimientoTemporal.objects.filter(solicitudes=obj.id)
        if(obj.establecimientos_temporales):
            # print self.__dict__

            # print "\n", obj.__dict__
            #print self.establecimientos_temporales
            # self.establecimiento=self.establecimientos_temporales
            establecimiento=obj.establecimientos
            establecimiento_temp=EstablecimientoTemporal.objects.get(id=obj.establecimientos_temporales.id)
            #establecimiento_temp=EstablecimientoTemporal.objects.filter(solicitudes=obj.id)
            if (establecimiento_temp.nombre):
                establecimiento.nombre        =  establecimiento_temp.nombre        
            if (establecimiento_temp.email):
                establecimiento.email        =  establecimiento_temp.email        
            if (establecimiento_temp.web_page):
                establecimiento.web_page        =  establecimiento_temp.web_page        
            if (establecimiento_temp.address):
                establecimiento.address        =  establecimiento_temp.address        
            if (establecimiento_temp.description):
                establecimiento.description        =  establecimiento_temp.description        
            if (establecimiento_temp.position):
                establecimiento.position=  establecimiento_temp.position
            if (establecimiento_temp.sub_categorias):
                establecimiento.sub_categorias=  establecimiento_temp.sub_categorias

            establecimiento.save()

            self.message_user(request,
                        _(("Se aprobó la solicitud de modificacion del establecimiento"+str(obj.establecimientos)).decode("utf-8")),
                         level=messages.INFO, extra_tags='', fail_silently=False)
            return True
        else:
            print "No se puede aprobar la modificacion."
            self.message_user(request,
                        _(("No Se aprobó la solicitud, el modificación para el establecimiento"+str(obj.establecimientos)).decode('utf-8')),
                         level=messages.INFO, extra_tags='', fail_silently=False)
            return False
        

    #Metodo cuandop se aprueba solicitud de administracion
    def aprobar_administracion(self,request,form,obj):
        """
            Apruba la administracón de un establecimiento.
        """
        if(obj.usuarios):            
            establecimientos=obj.establecimientos
            print Establecimiento.objects.filter(administradores=obj.usuarios.id,id=establecimientos.id)
            print "USUARIO ID ", obj.usuarios.id
            if  not (Establecimiento.objects.filter(administradores=obj.usuarios.id,id=establecimientos.id)):
                establecimientos.administradores.add(obj.usuarios)
                print obj.usuarios
            
                self.message_user(request,
                        _(("Se aprobó la solicitud, el usuario "+str(obj.usuarios)+" ya es administrador de "+str(obj.establecimientos)).decode("utf-8")),
                         level=messages.INFO, extra_tags='', fail_silently=False)

                if not obj.usuarios.is_organizacional() and  not obj.usuarios.is_superuser:
                    obj.usuarios.change_to_organizational()
                    obj.usuarios.save()
                    print "El usuario",obj.usuarios,"Se cambia a usuario organizacional"
                else:   
                    print "Mierda"

                return True
            else:
                self.message_user(request,
                        ("No Se aprobó la solicitud, el usuario "+str(obj.usuarios)+" es ahora administrador de "+str(obj.establecimientos)).decode("utf-8"),
                         level=messages.ERROR, extra_tags='', fail_silently=False)
                return False
        else:
            return False

    def response_delete(request, obj_display):
        """
            Redirige cuando eliminan establecimiento
        """
        return HttpResponseRedirect(reverse('admin:establishment_system'))


class ImagenAdmin(admin.ModelAdmin):
    u"""
        Clase encargada de presentar las imagines en el admin
    """
    list_display = ('id','imagen_thumbnail','establecimientos','date_uploaded','usuarios')       
    list_filter = ('usuarios', 'establecimientos', )
    search_fields = ('usuarios', 'establecimientos', )
    ordering = ('date_uploaded',)


    class Meta:
        model=Imagen

class CategoriasAdmin(admin.ModelAdmin):
    u"""
        Clase encargada de presentar las caegorias en el admin
    """
    list_display = ('id','tag',)  
    search_fields = ('tag', )

    class Meta:
        model=Categoria

class SubCategoriasAdmin(admin.ModelAdmin):
    u"""
        Clase encargada de presentar las caegorias en el admin
    """
    list_display = ('id','tag','categorias',)       
    list_filter = ('categorias', )
    search_fields = ('nombre', 'tag', )

    class Meta:
        model=SubCategoria

class TipoSolicitudAdmin(admin.ModelAdmin):
    u"""
        Clase encargada de presentar las caegorias en el admin
    """
    list_display = ('id','tag',)       
    list_filter = ('tag', )
    search_fields = ('nombre', 'tag', )

    class Meta:
        model=TiposSolicitud


admin.site.register(Categoria, CategoriasAdmin)
admin.site.register(SubCategoria, SubCategoriasAdmin)
admin.site.register(Imagen,ImagenAdmin)
admin.site.register(EstablecimientoTemporal)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(TiposSolicitud,TipoSolicitudAdmin)
admin.site.register(Comentario, CommentAdmin)



"""
    Modificación del mapa de GeoDjango
"""
from django.contrib.gis import admin 
from django.contrib.gis.geos import GEOSGeometry


class EstablecimientoAdmin(admin.OSMGeoAdmin): 
    g = GEOSGeometry('POINT (-74.157175 4.578896)') # Set map center 
    g.set_srid(4326) 
    #g.transform(900913) 
    default_lon = int(g.x) 
    default_lat = int(g.y) 
    default_zoom = 11 
    extra_js = ["http://maps.google.com/maps/api/js?key=AIzaSyCvfyKIBeaLLGXbF5HS73ZcfmDhPtM05rA&sensor=true"] 
    map_template = 'admin/gmgdav3.html'

    list_display = ('nombre','id','email','web_page','address','visible','sub_categorias')
    filter_horizontal=('administradores',)
    form=EstablecimientoAdminForm
    list_select_related = ('imagen',)
    inlines = [ ImagenInline  ]

    list_filter = ('visible','sub_categorias' )    
    search_fields = ('nombre','web_page','address', )
    
        
    class Media:
        js = (    
            'http://code.jquery.com/jquery-2.1.1.min.js', # jquery
            'js/update_categoria_admin.js',       # project static folder
        )


admin.site.register(Establecimiento, EstablecimientoAdmin) 