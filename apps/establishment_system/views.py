# -*- encoding: utf-8 -*-
from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.views.generic import DetailView, CreateView , ListView, UpdateView
from .models import Establecimiento, Comentario,  Imagen
from .forms import  ComentarioForm, CategoriasForm
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import datetime
from django.forms import DateField
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        context['establecimiento'] =Establecimiento
        comentarios=Comentario.objects.filter(post=establecimiento,is_public=True)
        usuario = self.request.user
        usuario_comentario=Comentario.objects.filter(author=usuario,post=establecimiento)
        
       
        
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



def eliminar_comentario(request,establecimiento_id=None, comentario_id=None):
    print establecimiento_id
    print comentario_id
    comentario=Comentario.objects.filter(author=request.user.id,post=establecimiento_id,id=comentario_id)
    print comentario
    #Si comentario  no esta vacio
    if ( comentario):
        print "Puede eliminar el comentario"
        comentario.delete()
    #De lo contrario
    else:
        print "No puede elimianr el comentario y esta intentando joder el sistema"

    return redirect('establecimiento_detail_url',pk=establecimiento_id)



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
    form_class = CategoriasForm
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



from django.contrib.auth.models import Group
from rest_framework import viewsets


from django.contrib.auth.models import Group
from rest_framework import serializers



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET', 'POST'])
def snippet_list(request,pk):
    print "ENTERO"
    try:
        snippet = Categoria.objects.get(pk=pk)
    except Exception, e:
        print "EROR : ",e

    if request.method == 'GET':
        serializer = CategoriaSerializer(snippet)
#        return Response(serializer.data)
        return JSONResponse(serializer.data)


    elif request.method == 'POST':
        serializer = CategoriaSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    

class UpdateEstablecimiento(UpdateView):
    model= Establecimiento
    template_name = "establishment/edit.html"
    content_type = None
    form_class = CategoriasForm
    success_url = lazy(reverse, str)("home_url")     