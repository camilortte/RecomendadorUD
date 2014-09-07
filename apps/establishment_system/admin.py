# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Categoria, Establecimiento, SubCategoria, Imagen ,EstablecimientoTemporal, Solicitud, TiposSolicitud,Solicitud
from .forms import EstablecimientoAdminForm
from .models import Comentario, Establecimiento, EstablecimientoTemporal, Imagen
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages 
#from fluent_comments.admin import FluentCommentsAdmin, CommentModel

#from django import forms
# from apps.djadmin_ext.helpers import BaseAjaxModelAdmin
# from apps.djadmin_ext.admin_forms import BaseAjaxModelForm


# class EstablecimientoAdminForm(BaseAjaxModelForm):
    
#     ajax_change_fields = ["categorias"]
#     categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),cache_choices=True)
#     sub_categorias= forms.ModelChoiceField(queryset=SubCategoria.objects.all(),cache_choices=True)

#     @property
#     def dynamic_fields(self):
#         selecte_categoria=  self.get_selected_value('categorias')
#         if not selecte_categoria:
#             return {}

#         sub_categorias = SubCategoria.objects.filter(categorias=selecte_categoria)
#         fields = {}
#         fields['sub_categorias'] = lambda:forms.ModelChoiceField(queryset=sub_categorias,cache_choices=True)
#         return fields

#     def create_field_and_assign_initial_value(self, queryset, selected_value):
#         return lambda: super(EstablecimientoAdminForm, self).create_field_and_assign_initial_value(queryset, selected_value)

#     class Meta(object):
#         model = Establecimiento

# class EstablecimientoAdmin(BaseAjaxModelAdmin):
#     form=CategoriasForm




class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('author','post' )

class ImagenInline(admin.StackedInline):
    model = Imagen

class EstablecimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre','email','web_page','address','visible','sub_categorias')
    filter_horizontal=('administradores',)
    form=EstablecimientoAdminForm
    list_select_related = ('imagen',)
    inlines = [ ImagenInline  ]
    
        
    class Media:
        js = (    
            'http://code.jquery.com/jquery-2.1.1.min.js', # jquery
            'js/update_categoria_admin.js',       # project static folder
        )

  

# class EstablecimientoTemporalInline(admin.StackedInline):
#     model = EstablecimientoTemporal

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
class SolicitudAdmin(admin.ModelAdmin):
    
    list_display = ('usuarios','establecimientos','tipo_solicitudes','aprobar')    
    #change_form_template = 'establishment/admin.html'
    #inlines = [ EstablecimientoTemporalInline  ]
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


    def change_view(self, request, object_id, form_url='', extra_context=None): 
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
    
    """Si la solicitud se aprobo ya no puede editarse"""
    def get_readonly_fields(self, request, obj=None):  
        if obj is not None :
            if obj.aprobar:
                return self.fields or [f.name for f in self.model._meta.fields]        
        return super(SolicitudAdmin, self).get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        print obj.aprobar
        if  obj.aprobar:
            try:
                if form.cleaned_data['aprobar'] == True:
                    print "ATRIBUTOS DE OBJ: ", obj.__dict__
                    print "SE aprobo la solicitud"
                    if form.cleaned_data['tipo_solicitudes'].nombre=='eliminacion':
                        print "ELIMINACION"            
                        if self.aprobar_eliminacion(request,form,obj):
                            obj.save()
                    elif form.cleaned_data['tipo_solicitudes'].nombre=='modificacion':
                        print "MODIFICACION"
                        if self.aprobar_modificacion(request,form,obj):      
                            obj.save()
                    elif form.cleaned_data['tipo_solicitudes'].nombre=='administracion':
                        print "Administracion"
                        if self.aprobar_administracion(request,form,obj):                            
                            obj.save()
                    elif form.cleaned_data['tipo_solicitudes'].nombre=='desactivacion':
                        print "desactivacion"
                        if self.aprobar_desactivacon(request,form,obj):     
                            print "ENTRO SAVE"                       
                            obj.save()

            except Exception, e:                                
                print "No se peude editar ",e     
                #raise e      
            
        else:
            obj.save()

    def aprobar_desactivacon(self,request,form,obj):           
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
        #establecimientos_temporales=EstablecimientoTemporal.objects.filter(solicitudes=obj.id)
        if(obj.establecimientos_temporales):
            # print self.__dict__

            # print "\n", obj.__dict__
            print "SE puede aprobar la modificacion"
            #print self.establecimientos_temporales
            # self.establecimiento=self.establecimientos_temporales
            print "Voy a inptimirt establecimientos:; "
            print obj.establecimientos
            print obj.establecimientos.id
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
            print "No se puede aprobar la modificacion paila"
            self.message_user(request,
                        _(("No Se aprobó la solicitud, el modificación para el establecimiento"+str(obj.establecimientos)).decode('utf-8')),
                         level=messages.INFO, extra_tags='', fail_silently=False)
            return False
        

    #Metodo cuandop se aprueba solicitud de administracion
    def aprobar_administracion(self,request,form,obj):
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
                return True
            else:
                self.message_user(request,
                        ("No Se aprobó la solicitud, el usuario "+str(obj.usuarios)+" es ahora administrador de "+str(obj.establecimientos)).decode("utf-8"),
                         level=messages.ERROR, extra_tags='', fail_silently=False)
                return False
        else:
            return False

    # #Redirige cuando eliminan establecimiento
    def response_delete(request, obj_display):
        return HttpResponseRedirect(reverse('admin:establishment_system'))


# class MyPost(Establecimiento):
#     class Meta:
#         proxy = True

# class MyPostAdmin(admin.ModelAdmin):
#     def queryset(self, request):
#         return Solicitud.objects.all()

# admin.site.register(MyPost, MyPostAdmin)

admin.site.register(Categoria)
admin.site.register(Establecimiento,EstablecimientoAdmin)
admin.site.register(SubCategoria)
admin.site.register(Imagen)
admin.site.register(EstablecimientoTemporal)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(TiposSolicitud)
admin.site.register(Comentario, CommentAdmin)
#admin.site.unregister(CommentModel)
#admin.site.register(CommentModel)#, CustomFluentCommentsAdmin)


# from tastypie.models import ApiKey
# from tastypie import admin as admintastypie

 
#admintastypie.site.unregister(ApiKey)
#admin.site.unregister(ApiAccess)

