# -*- encoding: utf-8 -*-
from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.views.generic import DetailView, CreateView , ListView, UpdateView, TemplateView, DeleteView
from .models import Establecimiento, Comentario,  Imagen, SubCategoria
from .forms import  ComentarioForm, EstablecimientoForm, CategoriasForm2, UploadImageForm, UploadImageForm
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import datetime
from django.forms import DateField
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.query import SearchQuerySet
from django.core.urlresolvers  import reverse_lazy , lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class probe(View):

    def get(self, request):
        return None

    def post(self, request):
 		return None

    def put(self, request):
        return None
 
    def delete(self, request):
        return None




class detalle_establecimiento(DetailView):
 
    #queryset = Establecimiento.objects.all()
    template_name = "establishment/detail.html"
    model= Establecimiento
    #slug_field= 'establecimiento_id'
    #slug_field_url='establecimiento_id'

    def get_context_data(self, **kwargs):
        context = super(detalle_establecimiento, self).get_context_data(**kwargs)
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
                print "Esta vacio"        
                context['form'] = ComentarioForm(initial=data)      
                print context['form']
            
            else:
                #No esta vacio no puede comentar
                #context['form'] = ComentarioForm(data=context['form'])      
                pass
            
        comentarios=Comentario.objects.filter(post=establecimiento,is_public=True)   
        paginator = Paginator(comentarios, 10) # Show 10 contacts per page
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

        
        
            
        return context



    # def dispatch(self, *args, **kwargs):
        
    #     return super(detalle_establecimiento, self).dispatch(*args, **kwargs)

    # def get_object(self):
    #     # Llamamos ala superclase
    #     object = super(detalle_establecimiento, self).get_object()
    #     # Grabamos el ultimo acceso ala base de datos
    #     #object.last_accessed = datetime.datetime.now()
    #     object.save()
    #     # Retornamos el objeto
    #     return object
class JSONMixin(object):



    def render_to_response(self, context, **httpresponse_kwargs):
        print "Entro render to response"
        return self.get_json_response(
            self.convert_context_to_json(context),
            **httpresponse_kwargs
        )

   
    def get_json_response(self, content, **httpresponse_kwargs):
        print "Entro render to response"
        return HttpResponse(
            content,
            content_type='application/json',
            **httpresponse_kwargs
        )

    def convert_context_to_json(self, context):
        u""" Este método serializa un formulario de Django y
        retorna un objeto JSON con sus campos y errores
        """
        print "CIONVEAAAAAAAAAAAAAAAAAAAAAAAAAA"
        form = context.get('form')
        to_json = {}
        options = context.get('options', {})
        to_json.update(options=options)
        print context
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
            print "Errres"
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
    model = Comentario
    form_class = ComentarioForm

    # once the user submits the form, validate the form and create the new user
    def post(self, request, *args, **kwargs):
        self.object = None
        # setup the form
        # we can use get_form this time as we no longer need to set the data property
        form = self.get_form(self.form_class)
        print "KAWARGS: ",kwargs
        print "ARGS; ",args
        self.establecimiento_id=kwargs['pk']
        self.success_url=reverse('establecimiento_detail_url',kwargs={'pk':self.establecimiento_id})   
        form.instance.author = self.request.user
        form.instance.post = Establecimiento.objects.get(id=self.establecimiento_id)

        if form.is_valid() and self.validate_comment():
            print "VALID FORM"
            return self.form_valid(form)
        else:
            print "INCALID FORM"
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(self.get_context_data(form=form))


    def validate_comment(self):
        print "VALIDATE COMETARIO"
        comentario=Comentario.objects.filter(author=self.request.user.id,post=self.establecimiento_id)
        print comentario
        if  not comentario:      
            #No existe ningun comentario
            return True
        else:
            #Si existe un comentario
            print "ESTA INTENTANDO JODER EL SISTEMA"
            return False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CommentCreateView, self).dispatch(*args, **kwargs)

from django.http import Http404,HttpResponseRedirect

class EliminarComentario(DeleteView):
    model = Comentario    

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
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
            print "No puede elimianr el comentario y esta intentando joder el sistema"
            raise Http404


        return {'comentario_id':comentario_id}

    # Override the delete function to delete report Y from client X
    # Finally redirect back to the client X page with the list of reports
    def delete(self, request, *args, **kwargs):        
        comentario_id = self.kwargs['comentario_id'] 
        establecimiento_id = self.kwargs['establecimiento_id'] 
        comentario=Comentario.objects.filter(author=request.user,
            post=Establecimiento.objects.get(id=establecimiento_id),
            id=comentario_id)
        #No esta vacio
        if  comentario:
            print comentario, "<---Comentarui"
            if comentario[0].author.id==request.user.id:
                comentario[0].delete()
            else:
                print "INTENTANDO JODER EL SISTEMA"
        if request.user.is_superuser:
            comentario=Comentario.objects.get(id=comentario_id)
            comentario.delete()
                            
        self.success_url = reverse('establecimiento_detail_url', kwargs={'pk': establecimiento_id})
        return HttpResponseRedirect(self.success_url)
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EliminarComentario, self).dispatch(*args, **kwargs)




class Establecimientoslist(ListView):
    paginate_by = 10
    model = Establecimiento
    template_name = "establishment/list.html"
    def get_context_data(self, **kwargs):
        context = super(Establecimientoslist, self).get_context_data(**kwargs)
        #context['now'] = timezone.now()
        return context


from vanilla import CreateView as CreateViewVanilla
from vanilla import TemplateView as TemplateViewVanilla
from django.utils.functional import lazy 

class CrearEstablecimiento(CreateViewVanilla):
    model= Establecimiento
    template_name = "establishment/create.html"
    content_type = None
    form_class = EstablecimientoForm
    success_url = lazy(reverse, str)("home_url") 
    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     # setup the form
    #     # we can use get_form this time as we no longer need to set the data property
    #     form = self.get_form(self.form_class)
    #     print form

    #     if form.is_valid() and self.validate_comment():
    #         print "VALID FORM"
    #         return self.form_valid(form)
    #     else:
    #         print "INCALID FORM"
    #         return self.form_invalid(form)


    def form_invalid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(CrearEstablecimiento, self).form_invalid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CrearEstablecimiento, self).dispatch(*args, **kwargs)


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
        print context
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
    model= Establecimiento
    template_name = "establishment/edit.html"
    content_type = None
    form_class = EstablecimientoForm
    success_url = lazy(reverse, str)("home_url")  

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateEstablecimiento, self).dispatch(*args, **kwargs)   



class CrearEstablecimiento2(CreateViewVanilla):
    model= Establecimiento
    template_name = "establishment/create2.html"
    content_type = None
    form_class = CategoriasForm2
    success_url = lazy(reverse, str)("home_url") 

    def form_invalid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(CrearEstablecimiento2, self).form_invalid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CrearEstablecimiento2, self).dispatch(*args, **kwargs)   


class Busqueda(TemplateView):
    template_name = "establishment/busqueda.html"


class Autocomplete(View):

    def get(self, request, *args, **kwargs):
        #print "ESTO LLEGA: ",request
        q=request.GET.get('q', None)
        print "query: ",q
        if q is not None and q != "":
            sqs = SearchQuerySet().autocomplete(nombre=q)[:10]
            sqs2 = SearchQuerySet().autocomplete(email=q)[:10]
            sqs3 = SearchQuerySet().autocomplete(web_page=q)[:10]
            sqs4 = SearchQuerySet().autocomplete(address=q)[:10]        
            
            establecimientos=[]
            establecimientos=self.get_establecimientis(establecimientos, sqs)
            establecimientos=self.get_establecimientis(establecimientos, sqs2)
            establecimientos=self.get_establecimientis(establecimientos, sqs3)
            establecimientos=self.get_establecimientis(establecimientos, sqs4)
        else:
            establecimientos =[]

        # Make sresult.ure you return a JSON object, not a bare list.
        # Otherwise, you could be vulnerable to an XSS attack.
        the_data = json.dumps({
            'results': establecimientos
        })
        return HttpResponse(the_data, content_type='application/json')

    def existe(self,establecimientos,id):
        #Obtener los ids valido para no repetir informacion
        for element in establecimientos:
            print element
            if element.get('id')==str(id):
                return True
        return False

    def get_establecimientis(self,establecimientos,sqs):
        for resultado in sqs:
            if not self.existe(establecimientos, resultado.pk):
                temporal={'id':resultado.pk,'nombre':resultado.nombre,'address':resultado.address,
                        'web_page':resultado.web_page,'email':resultado.email,'sub_categorias':resultado.sub_categorias}
                establecimientos.append(temporal)

        return establecimientos

from .serializers import EstablecimientoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# class  EstablecimientoCreateApiView(generics.CreateAPIView):
#     queryset = Establecimiento.objects.all()
#     serializer_class = EstablecimientoSerializer
#     #permission_classes = (IsAdminUser,)


class EstablecimientoCreateApiView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def post(self, request, format=None):
        serializer = EstablecimientoSerializer(data=request.DATA)
        if serializer.is_valid():
            print "IS VALID"
            serializer.save()
            print serializer.data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

from apps.account_system.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
class CalificacionApiView(APIView):

    authentication_classes = (  SessionAuthentication, BasicAuthentication,)

    def get(self, request, pk,format=None):
        print "ASDASASAS"
        print request.user
        print "DATA: ", pk
        try: 
            establecimiento = Establecimiento.objects.get(id=pk)
            user=User.objects.get(id=request.user.id)                
            calificacion_usuario= establecimiento.rating.get_rating_for_user(user) 
            salida={
                    "ratin_estableicimiento":establecimiento.rating.get_rating(),
                    "rating_usuario":calificacion_usuario
            }   
        except Exception, e:            
            try:                
                salida={
                    "ratin_estableicimiento":establecimiento.rating.get_rating(),
                    "rating_usuario":0
                }           
            except Exception, e:                          
                print "RESPONSE: ",salida 
                salida={}
                print "ERROR: ",e  

        return Response(salida,status=status.HTTP_200_OK)

    def post(self, request, pk,format=None):
        print "ENTRADA NORMAL JAJAJ con id=",pk
        try:
            print request.DATA            
            calificacion = request.DATA.get("calificacion")
            respuesta=""
            establecimiento = Establecimiento.objects.get(id=pk)
            if calificacion:
                calificacion=int(calificacion)
                if calificacion>=1 and calificacion<=5 :                
                    establecimiento.rating.add(score=calificacion, user=request.user, ip_address=request.META['REMOTE_ADDR'])
                    respuesta="Calificacion realizada"
                    return Response(respuesta, status=status.HTTP_201_CREATED)
                else:
                    respuesta="Valor no valido"     
        except Exception, e:
            print "EL ESTABLEcimiento no existe"
            respuesta="Algo salio mal"
            print e

        return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)


class UploadField(View):
    def post(self, request,pk, *args, **kwargs):        
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            print "FOrm valida: "
            print "Pk: ",pk
            print "CONTENIDO DE IMAGEN: ",request.FILES['imagen']
            establecimiento=Establecimiento.objects.get(id=pk)
            Imagen.objects.create(imagen=request.FILES['imagen'],establecimientos=establecimiento)     
            print "TODO BIEN"
            return redirect('establecimiento_detail_url',pk=pk)
        else:       
            print "Form no valida"
            return redirect('establecimiento_detail_url',pk=pk)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UploadField, self).dispatch(*args, **kwargs)   

class UploadField2(APIView):

    authentication_classes = (  SessionAuthentication, BasicAuthentication,)

    def post(self, request, pk,format=None):
        print "ENTRADA NORMAL JAJAJ"
        try:
            print "DATA: ",request.DATA  
            print "FILES: ",request.FILES
            print pk
            establecimiento = Establecimiento.objects.get(id=pk)
            imagen_count=Imagen.objects.filter(usuarios=request.user,establecimientos=establecimiento).count()
            if imagen_count <settings.MAX_UPLOAD_PER_USER:
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
                            respuesta={"error":"La imagen no puede ser mayor a 5 MB"}
                else:
                    respuesta={"error":"No subio nada"}
            else:
                respuesta={"error":"Limite maximo de imagenes por usuario en este establecimiento"}
        except Exception, e:
            print "EL ESTABLEcimiento no existe"
            respuesta="Algo salio mal"
            print e

        return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)


from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Imagen)
def Imagen_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    print "ENTRO INSTANCIA"
    instance.imagen.delete(False)
    print "SALIO INSTNCIO"
