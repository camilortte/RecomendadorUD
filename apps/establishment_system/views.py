# -*- encoding: utf-8 -*-

"""
    
    Views: Encontramos todas las vistas del sistema de establecimientos.

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

import datetime
import json

#Django
from django.shortcuts import render,redirect
from django.views.generic.base import View, TemplateView
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.forms import DateField
from django.contrib.gis.geos import Polygon, GEOSGeometry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers  import reverse_lazy , lazy,reverse
from django.contrib import messages
from django.views.generic import (
    DetailView, CreateView , ListView, UpdateView,
    DeleteView)

#externals apps
from vanilla import CreateView as CreateViewVanilla
from vanilla import TemplateView as TemplateViewVanilla
from haystack.query import SearchQuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from notifications import notify

#Internal apps
from apps.account_system.models import User
from apps.recommender_system.models import EstablecimientosRecommender

#Serializers
from .serializers import EstablecimientoSerializer, PaginatedEstablecimientoSerializer

#Models
from .models import (
    Establecimiento, Comentario,  Imagen, SubCategoria, 
    Categoria, TiposSolicitud, Solicitud)

#Forms
from .forms import (
    ComentarioForm, EstablecimientoForm,  
    UploadImageForm, CategoriasFilterForm, 
    SolicitudForm, EstablecimientoTemporalForm)


class DetalleEstablecimientoView(DetailView):
    u"""
        Se encarga de mostrar todos los datos de un establecimiento (entre 
        ellos las images), ademas carga todos los forms como comentarios y
        rating requeridos para la correcta interacción.

        Hereda todo de DetailView

        Attributes:
            template_name (str): Plantilla que se cargará.
            model (Mode): Clase del modelo que se usará.            

    """

    template_name = "establishment/detail.html"
    model= Establecimiento


    def get_context_data(self, **kwargs):
        u"""
            Se agregan contenxtos como las  imagenes, los forms de
            agregar y eliminar imagenes así como tambien los forms
            de agregar y eliminar comentarios.

            Tambien se realiza la paginación de comentarios.

            Tambien realiza las respectiva validaciones de quien puede,
            eliminiar, y agregar.

        """
        context = super(DetalleEstablecimientoView, self).get_context_data(**kwargs)
        establecimiento = self.object
        context['imagenes'] = Imagen.objects.filter(establecimientos=establecimiento)
        count=Imagen.objects.filter(establecimientos=establecimiento).count()
        if count < settings.MAX_IMAGES_PER_PLACE:
            context['imagenes_nulas'] = range(count,settings.MAX_IMAGES_PER_PLACE)
        context['establecimiento'] =Establecimiento
        

        if self.request.user.is_authenticated():
            context['form_image'] = UploadImageForm            
            usuario = self.request.user
            usuario_comentario=Comentario.objects.filter(author=usuario,post=establecimiento)

            #esta vacio puede comentar
            if not usuario_comentario: 
                data = {
                    'sender':context['object'].id,  
                    'is_public':True
                }         
                context['form'] = ComentarioForm(initial=data)                      
            
            else:
                #No esta vacio no puede comentar    
                pass
            

            if self.request.user.is_organizacional():            
                propietario=Establecimiento.objects.filter(administradores=self.request.user,id=establecimiento.id)                
                if propietario:
                    #Es propietario del establecimiento
                    context['propietario']=True


        comentarios=Comentario.objects.filter(post=establecimiento,is_public=True)   
        paginator = Paginator(comentarios, settings.MAX_COMMENTS_PER_PAGE) # Show 10 contacts per page
        page = self.request.GET.get('page')
        try:
            comentarios = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            comentarios = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            comentarios = paginator.page(paginator.num_pages)
        context['comentarios'] = comentarios
        context['can_upload_image']=self.can_upload_image()

        return context


    def can_upload_image(self):
        """
            Se encarga de validar si es posible subir otra imagen
        """
        if self.request.user.is_authenticated():
            if self.object.imagen_set.all().count() >= settings.MAX_IMAGES_PER_PLACE:
                return False
            else:
                if self.request.user.is_superuser or self.object.administradores.filter(id=self.request.user.id):
                    return True
                else:
                    if Imagen.objects.filter(usuarios=self.request.user,establecimientos=self.object).count() >= settings.MAX_UPLOAD_PER_USER:
                        return False
            return True
        else:
            return False

    @method_decorator(cache_control(must_revalidate=True, no_cache=True, no_store=True)) 
    def dispatch(self, *args, **kwargs):
        return super(DetalleEstablecimientoView, self).dispatch(*args, **kwargs)

class JSONMixin(object):

    u"""
        JSONMixin es un mixin para enviar los comentarios mediante JSON.
    """

    def render_to_response(self, context, **httpresponse_kwargs):
        return self.get_json_response(
            self.convert_context_to_json(context),
            **httpresponse_kwargs
        )

   
    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(
            content,
            content_type='application/json',
            **httpresponse_kwargs
        )

    def convert_context_to_json(self, context):
        u""" 
            Este método serializa un formulario de Django y
            retorna un objeto JSON con sus campos y errores

            retorna un objecto JSON
        """
        form = context.get('form')
        to_json = {}
        options = context.get('options', {})
        to_json.update(options=options)
        fields = {}
        for field_name, field in form.fields.items():
            if isinstance(field, DateField) \
                    and isinstance(form[field_name].value(), datetime.date):
                fields[field_name] = \
                    unicode(form[field_name].value().strftime('%d.%m.%Y'))
            else:
                fields[field_name] = \
                    form[field_name].value() \
                    and unicode(form[field_name].value()) \
                    or form[field_name].value()

        to_json.update(fields=fields)

        if form.errors:
            errors = {
                'non_field_errors': form.non_field_errors(),
            }
            fields = {}
            for field_name, text in form.errors.items():
                fields[field_name] = text
            errors.update(fields=fields)
            to_json.update(errors=errors)
        else:
            to_json={}
            context['success'] = True

        to_json.update(success=context.get('success', False))
        print "RETORNA ", json.dumps(to_json)


        return json.dumps(to_json)


class CommentCreateView(JSONMixin, CreateView):

    u"""
        Se envcarga de crear un nuevo comentario, usa el mixisn JSON
        para crearlo con json.

        Atributes:
            model (Mode): Clase del modelo que se usará.   
            form_class (Form): La clase formulario para la creación. 
    """

    model = Comentario
    form_class = ComentarioForm

    # once the user submits the form, validate the form and create the new user
    def post(self, request, *args, **kwargs):
        u"""
            Validamos los datos del formulario y segun esto procedemos con la 
            creación del comentario.

            se usa la clase validate comment para validar.

            Returns:
                Llamado a la clase padre de form_valid si es valido el comentario
                De lo contrario se llama a la clase padre form_invalid()

        """
        self.object = None
        # setup the form
        # we can use get_form this time as we no longer need to set the data property
        form = self.get_form(self.form_class)
        # print "KAWARGS: ",kwargs
        # print "ARGS; ",args
        self.establecimiento_id=kwargs['pk']
        self.success_url=reverse('establecimiento_detail_url',kwargs={'pk':self.establecimiento_id})   
        form.instance.author = self.request.user
        form.instance.post = Establecimiento.objects.get(id=self.establecimiento_id)

        if form.is_valid() and self.validate_comment():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, u"Comentario creado.") 
        return self.render_to_response(self.get_context_data(form=form))


    def validate_comment(self):
        u"""            
            Se validan que el usuario no halla comentado anteriormente en el mismo
            establecimiento, 

            Returns:
                True si puede comentario
                False si ya comento y no pdra comentar
        """
        comentario=Comentario.objects.filter(author=self.request.user.id,post=self.establecimiento_id)
        print comentario
        if  not comentario:      
            #No existe ningun comentario
            return True
        else:
            #Si existe un comentario
            return False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CommentCreateView, self).dispatch(*args, **kwargs)

class EliminarEstablecimiento(DeleteView):
    u"""
        Clase encargada de eliminar un establecimiento solo por el usuario
        propietario 
    """
    model = Establecimiento    
    success_url=reverse_lazy('establecimientos_propios_ur')

    def get_object(self, queryset=None):
        u"""             
            Validamos que el objeto que se eliminará sea propiedad del
            usuario que lo elminará

            Returns:
                Context si el usuario es quien eliminara su propio establecimiento
                Http404 si es un usuario invalido intentnaod eliminar.
        """
        establecimiento_id= self.kwargs['pk']
        
        establecimiento=Establecimiento.objects.filter(id=establecimiento_id,administradores=self.request.user.id)

        if establecimiento and (self.request.user.is_organizacional or self.request.user.is_superuser ):
            context = super(EliminarEstablecimiento, self).get_object(queryset=None)
            return context
        #De lo contrario
        else:
            print "No puede elimianr el comentario y esta intentando romper el sistema"
            raise Http404

    def delete(self, request, *args, **kwargs):            
        ctx= super(EliminarEstablecimiento, self).delete(request,*args, **kwargs)
        messages.success(self.request, u"Establecimiento Eliminado.") 
        return ctx
                            
                
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EliminarEstablecimiento, self).dispatch(*args, **kwargs)


class EliminarComentario(DeleteView):

    u"""
        Clase para eliminar un comentario, este solo podrá ser eliminado
        por el autor, el propietario  del establecimiento o un usuario 
        administrador

        Atributes:
            model (Model): Modelo que se usará.
    """

    model = Comentario    

    def get_object(self, queryset=None):
        u"""             
            Validamos que el objeto que se eliminará sea propiedad del
            usuario que lo elminará

            Returns:
                Context si el usuario es quien eliminara su propio comentario
                Http404 si es un usuario invalido intentnaod eliminar.
        """
        establecimiento_id= self.kwargs['establecimiento_id']
        comentario_id= self.kwargs['comentario_id']
        #obj = super(EliminarComentario, self).get_object()

        comentario=Comentario.objects.filter(author=self.request.user.id,post=establecimiento_id,id=comentario_id)
        #Si comentario  no esta vacio
        if ( comentario):
            #comentario.delete()
            context = {'establecimiento_id':establecimiento_id, 'comentario_id':comentario_id}
            return context
        #De lo contrario
        else:
            print "No puede elimianr el comentario y esta intentando romper el sistema"
            raise Http404

        return {'comentario_id':comentario_id}

    
    def delete(self, request, *args, **kwargs):    
        u"""
            se comprueba que el comentario a eliminar sea eliminado por el propietario del comentario
            o por un usuario administrador. Si todo es valido se eliminara.

            Returns:
                HttpResponseRedirect A el establecimiento que alojó el comentario.
        """    
        comentario_id = self.kwargs['comentario_id']         
        establecimiento_id = self.kwargs['establecimiento_id'] 
        if request.user.is_superuser:
            comentario=Comentario.objects.get(id=comentario_id)
            comentario.delete()
        else:            
            comentario=Comentario.objects.filter(author=request.user,
                post=Establecimiento.objects.get(id=establecimiento_id),
                id=comentario_id)
            #No esta vacio
            if  comentario:
                if comentario[0].author.id==request.user.id:
                    comentario[0].delete()
                            
        messages.success(self.request, u"Comentario Eliminado.") 
        self.success_url = reverse('establecimiento_detail_url', kwargs={'pk': establecimiento_id})
        return HttpResponseRedirect(self.success_url)
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EliminarComentario, self).dispatch(*args, **kwargs)




class Establecimientoslist(ListView):

    u"""
        Lista  los establecimientos en el sisitema, segun los criterios de busqueda.

        Atributes:
            paginate_by (int): Numero de establecimientos por pagina.
            model (Model): Modelo 
            template_name (String): Template donde se carga la información
    """

    paginate_by = 10
    model = Establecimiento
    template_name = "establishment/list.html"

    def get_context_data(self, **kwargs):
        u"""
            Se agrega el contenxto el formulario de categorias
        """
        context = super(Establecimientoslist, self).get_context_data(**kwargs)
        #context['now'] = timezone.now()
        context['form_categorias']=CategoriasFilterForm
        return context


class CrearEstablecimiento(CreateViewVanilla):
    u"""
        Crea un nuevo establecimiento
    """
    model= Establecimiento
    template_name = "establishment/create.html"
    content_type = None
    form_class = EstablecimientoForm
    success_url = lazy(reverse, str)("home_url")   #Esta se modifica en el metodo get_succes_url

    

    def get_success_url(self):        
        messages.success(self.request, u"Establecimiento creado.")  
        return reverse_lazy('establecimiento_detail_url',
                            kwargs={'pk': self.object.id})

    def form_invalid(self, form):
        return super(CrearEstablecimiento, self).form_invalid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CrearEstablecimiento, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        u"""
            Se agregan los contexto de longitud y latitud
        """
        ctx = super(CrearEstablecimiento, self).get_context_data(**kwargs)
        form=kwargs.get('form')
        position= form.instance.position
        if position is not None:
            pnt = GEOSGeometry(position) # WKT        
            ctx['lng'] = pnt.y
            ctx['lat'] = pnt.x
        return ctx

#################NO SE PARA QUE SE USA#########################################<------------------------------------------------------------------------------------------------------------------------------------
class RecargarDatosEstablecimiento(TemplateViewVanilla):

    def render_to_response(self, context, **httpresponse_kwargs):
        return self.get_json_response(
            self.convert_context_to_json(context),
            **httpresponse_kwargs
        )

   
    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(
            content,
            content_type='application/json',
            **httpresponse_kwargs
        )

    def convert_context_to_json(self, context):
        u""" Este método serializa un formulario de Django y
        retorna un objeto JSON con sus campos y errores
        """
        form = context.get('form')
        to_json = {}
        options = context.get('options', {})
        to_json.update(options=options)
        fields = {}
        for field_name, field in form.fields.items():
            if isinstance(field, DateField) \
                    and isinstance(form[field_name].value(), datetime.date):
                fields[field_name] = \
                    unicode(form[field_name].value().strftime('%d.%m.%Y'))
            else:
                fields[field_name] = \
                    form[field_name].value() \
                    and unicode(form[field_name].value()) \
                    or form[field_name].value()

        to_json.update(fields=fields)

        if form.errors:
            errors = {
                'non_field_errors': form.non_field_errors(),
            }
            fields = {}
            for field_name, text in form.errors.items():
                fields[field_name] = text
            errors.update(fields=fields)
            to_json.update(errors=errors)
        else:
            to_json={}
            context['success'] = True

        to_json.update(success=context.get('success', False))        


        return json.dumps(to_json)

    

class UpdateEstablecimiento(UpdateView):

    u"""
        Actualizar los datos de un establecimientos
    """

    model= Establecimiento
    template_name = "establishment/edit.html"
    content_type = None
    form_class = EstablecimientoForm
    success_url = lazy(reverse, str)("home_url")   #Esta se modifica en el metodo get_succes_url

    def get_success_url(self):        
        messages.success(self.request, u"Establecimiento Actualizado.") 
        return reverse_lazy('establecimiento_detail_url',
                            kwargs={'pk': self.object.id})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateEstablecimiento, self).dispatch(*args, **kwargs)   

    def get_context_data(self, **kwargs):
        u"""
            Se agregan los contexto de longitud y latitud
        """
        ctx = super(UpdateEstablecimiento, self).get_context_data(**kwargs)
        pnt = GEOSGeometry(self.object.position) # WKT        
        ctx['lng'] = pnt.y
        ctx['lat'] = pnt.x

        return ctx

    def get_object(self, queryset=None):
        u"""
            Solo puede actualizar los datos un usuario organizacional dueño del
            establecimiento o un usuario administrador

            Returns:
                Establecimiento object si es valido
                Http404 si no es valido
        """
        if self.request.user.is_superuser:
            #Si el usuario es administrador
            obj = super(UpdateEstablecimiento, self).get_object()
        else:            
            #Si es organizacional
            if self.request.user.is_organizacional():
                obj = super(UpdateEstablecimiento, self).get_object()            
                establecimientos=Establecimiento.objects.filter(administradores=self.request.user, id=obj.id)
                if not establecimientos:
                    raise Http404
            else:
                print "Intentando romper el sistema"
                raise Http404
        return obj



# class CrearEstablecimiento2(CreateViewVanilla):

#     u"""
#         DEPRECATE
#         ---------

#         Crear un establecimiento mediante JSON y AJAX
#     """

#     model= Establecimiento
#     template_name = "establishment/create2.html"
#     content_type = None
#     form_class = CategoriasForm2
#     success_url = lazy(reverse, str)("home_url") 

#     def form_invalid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         return super(CrearEstablecimiento2, self).form_invalid(form)

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(CrearEstablecimiento2, self).dispatch(*args, **kwargs)   



# class Busqueda(TemplateView):
#     template_name = "establishment/busqueda.html"


class Autocomplete(View):

    u"""
        Se encarga de autocompletar  la busqueda mediante JSON.
    """

    def get(self, request, *args, **kwargs):        
        u"""
            Se realizan los querys de la bsuqueda de la siguiente manera:
            sqs--> Se buscan los nombres que coincidan con el caracter de busqueda
            sq1--> Se buscan el email que coincidan con el caracter de busqueda
            sqs2--> Se buscan la pagina web que coincidan con el caracter de busqueda
            sqs3--> Se buscan la direccion que coincidan con el caracter de busqueda

            TODO:
                Se planea agregar Categorias y sub categorias en la busqueda.

            Notes: 
                Tener cudado en devolver un objecto JSON y no el de python,
                ya que es propenso a ataque XSS.

            Returns:
                Objeto JSON con los resultados de las coincidencias
        """
        q=request.GET.get('q', None)
        if q is not None and q != "":

            sqs = SearchQuerySet().autocomplete(nombre__icontains=q)[:10]
            sqs = SearchQuerySet().autocomplete(nombre=q)[:10]        
            # sqs2 = SearchQuerySet().autocomplete(email=q)[:10]
            # sqs3 = SearchQuerySet().autocomplete(web_page=q)[:10]
            # sqs4 = SearchQuerySet().autocomplete(address=q)[:10]        
            # sqs5 = SearchQuerySet().autocomplete(sub_categorias=q)[:10]        
            # sqs5 = SearchQuerySet().autocomplete(tag=q)[:10]    
            
            establecimientos=[]
            establecimientos=self.get_establecimientis(establecimientos, sqs)
            # establecimientos=self.get_establecimientis(establecimientos, sqs2)
            # establecimientos=self.get_establecimientis(establecimientos, sqs3)
            # establecimientos=self.get_establecimientis(establecimientos, sqs4)
            # establecimientos=self.get_establecimientis(establecimientos, sqs5)
            # establecimientos=self.get_establecimientis(establecimientos, sqs5)
        else:            
            # categoria=Categoria.objects.filter(tag__icontains=q)
            # sub_cate=SubCategoria.objects.filter(categorias=categoria)
            # query=establecimientos.objects.filter(sub_categorias=sub_cate)
            # if query:
            #     establecimientos=query
            # else:
            #     establecimientos =[]
            establecimientos= []

        # Make sresult.ure you return a JSON object, not a bare list.
        # Otherwise, you could be vulnerable to an XSS attack.
        the_data = json.dumps({
            'results': establecimientos
        })
        return HttpResponse(the_data, content_type='application/json')

    def existe(self,establecimientos,id):
        """
            Obtener los ids valido para no repetir informacion
        """
        for element in establecimientos:
            if element.get('id')==str(id):
                return True
        return False

    def get_establecimientis(self,establecimientos,sqs):
        u"""
            Se encarga de agregar nuevos resultado(Establecmientos) sin repetirlos
        """
        for resultado in sqs:
            if not self.existe(establecimientos, resultado.pk):
                temporal={'id':resultado.pk,'nombre':resultado.nombre,'address':resultado.address,
                        'web_page':resultado.web_page,'email':resultado.email,'sub_categorias':resultado.sub_categorias}
                establecimientos.append(temporal)

        return establecimientos


class DeleteImagen(DeleteView):

    u"""
        Elimianr una imagen de un establecimiento
    """

    model=Imagen
    success_url = reverse_lazy('home_url')

    def get_object(self, queryset=None):
        u""" 
            Se valida que el que elimine sea quien subió la imange,
            un usuario organizacional o un usuario administrador.

            Returns:
                Establecimiento object si es valido.
                Http404 raise si es invalido.
        """
        if self.request.user.is_superuser:
            #Si el usuario es administrador
            obj = super(DeleteImagen, self).get_object()
        else:            
            obj = super(DeleteImagen, self).get_object()
            imagen = Imagen.objects.filter(usuarios=self.request.user,id=obj.id)
            #Si el usuario es propietario de la imagen
            if  imagen:
                #Si hay coincidencias
                pass
            else:
                #Si el usuario es dueno del establecimiento
                if self.request.user.is_organizacional:
                    establecimientos=Establecimiento.objects.filter(administradores=self.request.user)
                    if establecimientos:
                        obj = super(DeleteImagen, self).get_object()
                    else:
                        print "Intentando romper el sistema"
                        raise Http404
                else:
                    print "Intentando romper el sistema"
                    raise Http404
        print " SE BORRARA LA IMAGEN: ",obj.id
        messages.success(self.request, u"Imagen eliminada.") 
        self.success_url=reverse_lazy('establecimiento_detail_url',
                            kwargs={'pk': self.kwargs['est_id']})
        return obj

    
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteImagen, self).dispatch(*args, **kwargs)


from datetime import datetime as mydatetime
class Solicitar(View):
    u"""
       Se encarga de crear una solicitud depenedindo de esta. 
       Tiene los metodos GET y POST
    """

    def get(self, request,tipo_solicitud,establecimiento_id):
        u"""
            Se cargan los formularios dependiendo del tipo de solicitud;
            0 --> Solicitud administracion establecimiento
            1 --> Solicitud de edicion del establecimiento, se agrega 
                  en el contexto el formulario de edicion y la longitud
                  y latitud actuales del establecimiento.
            2 --> Solicitud de eliminacion por repeticion
            3 --> Solicitud de eliminacion por inexistencia.

            En todas las solicitudes se agrega un formulario de solicitud.
        """
        establecimiento=Establecimiento.objects.get(id=establecimiento_id)
        if tipo_solicitud=='0':
            formulario= SolicitudForm()
        else: 
            if tipo_solicitud=='1' and establecimiento_id:                
                formulario= SolicitudForm()                
                est=Establecimiento.objects.get(id=establecimiento_id)
                lng=est.position.y
                lat=est.position.x
                formulario2= EstablecimientoTemporalForm(instance=est)
                return render(request, 'establishment/solicitud.html', {
                    'form':formulario, 'form2':formulario2,
                    'lng':lng,'lat':lat,
                    'tipo_solicitud':tipo_solicitud,
                    'establecimiento':establecimiento
                })
            else: 
                if tipo_solicitud=='2':
                    formulario= SolicitudForm()
                else: 
                    if tipo_solicitud=='3':
                        formulario= SolicitudForm()
                    else:
                        raise Http404               
        
        return render(request, 'establishment/solicitud.html', 
            {'form':formulario, 
                'tipo_solicitud':tipo_solicitud,
                'establecimiento':establecimiento
            })

    def post(self, request,tipo_solicitud,establecimiento_id):
        u"""
            Dependiendo del request se realizan las acciones
            0 --> Solicitud administracion establecimiento
            1 --> Solicitud de edicion del establecimiento
            2 --> Solicitud de eliminacion por repeticion
            3 --> Solicitud de eliminacion por inexistencia.
        """
        enviada=False
        tipo=""
        id_EstablecimientoTemporal=None
        if request.user.is_authenticated():            
            """Solicitud de administracion"""
            if tipo_solicitud=='0':
                formulario= SolicitudForm(request.POST)
                if formulario.is_valid():
                    enviada=True
                    tipo="administracion"
            else: 
                """Solictud de edicion del establecimiento"""
                if tipo_solicitud=='1':
                    formulario= SolicitudForm(request.POST)     
                    formulario2= EstablecimientoTemporalForm(request.POST)#Establecimieto temporal
                    if formulario2.is_valid():
                        id_EstablecimientoTemporal=formulario2.save() 
                        if formulario.is_valid():                       
                            enviada=True
                            tipo="modificacion"
                        else:               
                            pnt = GEOSGeometry(formulario2.cleaned_data['position']) # WKT
                            lng=pnt.y
                            lat=pnt.x
                            formulario=SolicitudForm(data=request.POST)
                            formulario2= EstablecimientoTemporalForm(data=request.POST)
                            return render(request, 'establishment/solicitud.html', {
                                    'form':formulario, 'form2':formulario2,
                                    'lng':lng,'lat':lat
                                })


                else: 
                    if tipo_solicitud=='2':
                        formulario= SolicitudForm(request.POST)
                        if formulario.is_valid():
                            enviada=True
                            tipo="eliminacion"
                    else: 
                        if tipo_solicitud=='3':
                            formulario= SolicitudForm(request.POST)
                            if formulario.is_valid():
                                enviada=True
                                tipo="eliminacion"
                        else:
                            raise Http404

        if enviada and tipo != "":
            notify.send(
                request.user,
                recipient= request.user,
                verb="Solicitud Enviada",                    
                description="Hola "+request.user.first_name+" para informarte que estamos mirando tu"\
                "e solicitud de "+tipo+", gracias por tu paciencia.",
                timestamp=mydatetime.now()
            ) 
            
            
            if not id_EstablecimientoTemporal:                
                self.create_solicitud(tipo.title()+formulario.cleaned_data['contenido'],
                     request.user, establecimiento_id, tipo)
            else:
                
                self.create_solicitud(tipo.title()+formulario.cleaned_data['contenido'],
                     request.user, establecimiento_id, tipo,id_EstablecimientoTemporal)

            messages.success(self.request, u"Solicitud enviada.") 
            return redirect('/establecimientos/'+establecimiento_id+'/')
            

        formulario=SolicitudForm(data=request.POST)
        formulario2= EstablecimientoTemporalForm(data=request.POST)
        return render(request, 'establishment/solicitud.html', {
                'form':formulario, 'form2':formulario2,
            })

   
    def create_solicitud(self,contenido,user,establecimiento_id,tipo_solicitud,establecimientos_temporales=None):
        u"""
            Se crear un nueva solicitud dependiendo si es de edicion o de las demas.
        """
        if establecimientos_temporales is None:
            Solicitud.objects.create(
                    contenido=contenido,
                    usuarios=user,
                    establecimientos=Establecimiento.objects.get(id=establecimiento_id),
                    tipo_solicitudes=TiposSolicitud.objects.get(nombre=tipo_solicitud)
            )
        else:
            Solicitud.objects.create(
                    contenido=contenido,
                    usuarios=user,
                    establecimientos=Establecimiento.objects.get(id=establecimiento_id),
                    tipo_solicitudes=TiposSolicitud.objects.get(nombre=tipo_solicitud),
                    establecimientos_temporales=establecimientos_temporales,
            )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Solicitar, self).dispatch(*args, **kwargs)
           



class EstablecimientosPropios(ListView):
    u"""
        Carga los establecimientos propios de un usuario organizacional.
    """

    paginate_by = 10
    model = Establecimiento
    template_name = "establishment/list_own.html"
    context_object_name = "establecimientos_propios" 

    def get_context_data(self, **kwargs):
        """
            Se agrega el contexto del formulario de categorias 
        """
        context = super(EstablecimientosPropios, self).get_context_data(**kwargs)
        #context['now'] = timezone.now()
        context['form_categorias']=CategoriasFilterForm
        return context

    def get_queryset(self):
        """
            Se filtra los establecimientos por el propietario del request
        """
        query=Establecimiento.objects.filter(administradores=self.request.user)
        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EstablecimientosPropios, self).dispatch(*args, **kwargs)



class UploadImagenView(View):
    u"""
        DEPRECATE
            ---------

            Subir una imagen 
    """
    def post(self, request,pk, *args, **kwargs):        
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # print "FOrm valida: "
            # print "Pk: ",pk
            # print "CONTENIDO DE IMAGEN: ",request.FILES['imagen']
            establecimiento=Establecimiento.objects.get(id=pk)
            Imagen.objects.create(imagen=request.FILES['imagen'],establecimientos=establecimiento)                 
            return redirect('establecimiento_detail_url',pk=pk)
        else:       
            return redirect('establecimiento_detail_url',pk=pk)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UploadImagenView, self).dispatch(*args, **kwargs)   

from django.db.models import Q
class BusquedarView(TemplateView):
    template_name = "establishment/busqueda.html"

    def get(self, request, *args, **kwargs):
        q=request.GET.get('q',None)      
        if q is not None:
            establecimientos=Establecimiento.objects.filter(
                Q(nombre__icontains=q) | Q(email__icontains=q) | 
                Q(address__icontains=q) | Q(email__icontains=q) | 
                Q(sub_categorias__icontains=SubCategoria.objects.filter(tag__icontains=q)))

            
            paginator = Paginator(establecimientos, 20)
            page = request.GET.get('page')
            try:
                establecimientos = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                establecimientos = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                establecimientos = paginator.page(paginator.num_pages)
        else:
            establecimientos=None

        return render(request, "establishment/busqueda.html",{'datos':establecimientos,'query':q})

    
    def existe(self,establecimientos,id):
        """
            Obtener los ids valido para no repetir informacion
        """
        for element in establecimientos:
            if element.get('id')==str(id):
                return True
        return False

    def get_establecimientis(self,establecimientos,sqs):
        u"""
            Se encarga de agregar nuevos resultado(Establecmientos) sin repetirlos
        """
        for resultado in sqs:
            if not self.existe(establecimientos, resultado.pk):
                temporal={'id':resultado.pk,'nombre':resultado.nombre,'address':resultado.address,
                        'web_page':resultado.web_page,'email':resultado.email,'sub_categorias':resultado.sub_categorias}
                establecimientos.append(temporal)

        return establecimientos


#################################################################################################
#####################################################                 ###########################
#####################################################    APIS VIEWS   ###########################
#####################################################                 ###########################
#################################################################################################

class EstablecimientoCreateApiView(APIView):
    u"""
        DEPRECATE
        ---------

        Crear un establecimiento mediante REST
    """

    def post(self, request, format=None):
        serializer = EstablecimientoSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  


class CalificacionApiView(APIView):

    u"""
        Calificar un establecimiento median JSON soportado por REST

        Attributes:
            authentication_classes (AthenticacionRest): Tipos de autenticacion para poder calificar
    """

    authentication_classes = (  SessionAuthentication, BasicAuthentication,)

    def get(self, request, pk,format=None):
        u"""
            Obiene las calificaciones realizadas por un usuario en concreto y el procentaje total
            de calificacines del establecimiento en concreto.

            Returns:
                Si todo es correcto retorna un objeto JSON con los datos, de lo contrario
                retorna vacio
        """        
        
        try: 
            establecimiento = Establecimiento.objects.get(id=pk)
            user=User.objects.get(id=request.user.id)                
            calificacion_usuario= establecimiento.rating.get_rating_for_user(user) 
            salida={
                    "ratin_estableicimiento":round(establecimiento.rating.get_rating(),1),
                    "rating_usuario":calificacion_usuario
            }   
        except Exception, e:            
            try:                
                salida={
                    "ratin_estableicimiento":round(establecimiento.rating.get_rating(),1),
                    "rating_usuario":0
                }           
            except Exception, e:                                          
                salida={}
                print "ERROR: ",e  

        return Response(salida,status=status.HTTP_200_OK)

    def post(self, request, pk,format=None):
        u"""
            Se modifica una calificacion si existe , de lo contrario se crea una nueva.

            Returns:
                Ok HTTP_201_CREATED si to salio bien, 
                de lo contrario HTTP_400_BAD_REQUEST
        """
        
        try:                      
            calificacion = request.DATA.get("calificacion")
            respuesta=""            
            establecimiento = Establecimiento.objects.get(id=pk)            
            if calificacion:
                calificacion=int(calificacion)
                if calificacion>=1 and calificacion<=5 :    
                    recommender=EstablecimientosRecommender()        
                    establecimiento.rating.add(
                        score=calificacion, 
                        user=request.user, 
                        ip_address=request.META['REMOTE_ADDR']
                        )                                                         
                    recommender.precompute()                 
                    respuesta="Calificacion realizada"
                    return Response(respuesta, status=status.HTTP_201_CREATED)
                else:
                    respuesta="Valor no valido"     
        except Exception, e:
            print "El establecimiento no existe"
            respuesta="Algo salio mal"
            print e
        return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)




class UploadImagenApiView(APIView):
    u"""
        Subir una imagen median REST por JSON
    """

    authentication_classes = (  SessionAuthentication, BasicAuthentication,)

    def post(self, request, pk,format=None):
        u"""
            Se valida que la imagen cumpla los requisitos (jpeg,pjpeg,png,jpg) menor o igual
            a 5 MB, el usuario convencional no podra subir mas de 3 imagenes y el establecimientono 
            no tendrá más de 8 imagenes
        """
        
        try:
            establecimiento = Establecimiento.objects.get(id=pk)
            imagen_count=Imagen.objects.filter(usuarios=request.user,establecimientos=establecimiento).count()
            propietario=establecimiento.administradores.filter(id=request.user.id)
            if establecimiento.imagen_set.count() < settings.MAX_IMAGES_PER_PLACE: 
                if imagen_count <settings.MAX_UPLOAD_PER_USER or self.request.user.is_superuser or propietario:
                    if request.FILES:
                        #imagen = request.FILES.get("imagen")
                        imagen= request.FILES[u'file']
                        size=int(imagen.size)

                        #validate content type
                        main, sub = imagen.content_type.split('/')
                        if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                            respuesta={"error":'Please use a JPEG, JPG or PNG image.'}
                        else:
                            if size <= settings.MAX_UPLOAD_SIZE:
                                respuesta=""
                                
                                element=Imagen(imagen=imagen,establecimientos=establecimiento,usuarios=request.user)    
                                element.save()
                                respuesta="OK"
                                return Response(respuesta, status=status.HTTP_201_CREATED)
                            else:
                                print "Supera el tamanio de la image."
                                respuesta={"error":"La imagen no puede ser mayor a 10 MB"}
                    else:
                        respuesta={"error":"No subio nada"}
                else:
                    respuesta={"error":"Limite maximo de imagenes por usuario en este establecimiento"}
            else:
                respuesta={"error":"Limite maximo de imagenes para el establecimiento"}
        except Exception, e:
            print "EL ESTABLEcimiento no existe"
            respuesta="Algo salio mal"
            print e

        return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)


class EstablecimientosByBoung(APIView):
    u"""
        Se encarga de mostrar los establecimiento  que se encuentran en la zona visible
        de google maps, esto lo realiza mediante los boungs  y una consulta del tipo
        de base de datos geos. 

        Todo se hace por JSON
    """

    def get(self, request, format=None):
        u"""
            Obtiene los boung y realzia la consulta, ordena la consulta por rating_score

            Returns:
                JSON object.
        """
        # boung_data_x1 = request.GET.get("x1",None)
        # boung_data_y1 = request.GET.get("y1")
        # boung_data_x2 = request.GET.get("x2")
        # boung_data_y2 = request.GET.get("y2")

        boung_data_x1 = request.GET.get("y1",None)
        boung_data_y1 = request.GET.get("x1")
        boung_data_x2 = request.GET.get("y2")
        boung_data_y2 = request.GET.get("x2")

        

        number_page=request.GET.get("pagina",None)
        if number_page is None:
            number_page=1

        # print "boung_data_x1: ",boung_data_x1
        # print "boung_data_y1: ",boung_data_y1
        # print "boung_data_x2: ",boung_data_x2
        # print "boung_data_y1: ",boung_data_y2
        if boung_data_x1 is not None:

            nombre=request.GET.get("nombre",None)
            categoria=request.GET.get("categoria",None)
            sub_categoria=request.GET.get("sub_categoria",None)

            # print "Valores: "
            # print "Nombre: ",nombre
            # print "Categoria: ",categoria
            # print "sub_categoria: ",sub_categoria

            box=Polygon.from_bbox((boung_data_x1,boung_data_y1,boung_data_x2,boung_data_y2))
            query=Establecimiento.objects.filter(position__within=box,visible=True).order_by('rating_score')
            if nombre:
                query=query.filter(nombre__icontains=nombre)            
            if sub_categoria:
                query=query.filter(sub_categorias=sub_categoria)
            else:
                if categoria:
                    categoria=Categoria.objects.get(id=categoria)
                    sub_cate=SubCategoria.objects.filter(categorias=categoria)
                    query=query.filter(sub_categorias=sub_cate)
            paginator = Paginator(query, settings.ITEMS_PAGINATE)
            query=paginator.page(number_page)
            serializer=PaginatedEstablecimientoSerializer(query)
            salida=serializer.data
            #print "Respuesta: ",salida
        else:
            salida={"error":"None"}       

        return Response(salida,status=status.HTTP_200_OK)


###########################################################################################
#####################################################                 #####################
#####################################################    SIGNALS      #####################
#####################################################                 #####################
###########################################################################################
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from apps.externals.djangoratings.models import Vote, Score

@receiver(pre_delete, sender=Imagen)
def Imagen_delete(sender, instance, **kwargs):
    u"""
        Cuando una imagen se borrar tambíen se borrara en el disco.
    """
    instance.imagen.delete(False)

@receiver(pre_delete, sender=Establecimiento)
def establecimiento_delete(sender, instance, **kwargs):
    u"""
        Cuando una establecimiento se borra tambíen se borrara los votos
    """
    id_establecimiento=instance.id
    Vote.objects.filter(object_id=id_establecimiento).delete()
    Score.objects.filter(object_id=id_establecimiento).delete()
    recommender=EstablecimientosRecommender()    
    recommender.precompute()



