from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import DetailView
from .models import Establecimiento, Comentario, SubCategoria, Imagen


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
    template_name = "establishment/base.html"
    model= Establecimiento
    #slug_field= 'establecimiento_id'
    #slug_field_url='establecimiento_id'

    def get_context_data(self, **kwargs):
        context = super(detalle_establecimiento, self).get_context_data(**kwargs)
        establecimiento = self.object
        context['imagenes'] = Imagen.objects.filter(establecimientos=establecimiento)
        context['establecimiento'] =Establecimiento
        return context


    # def get_object(self):
    #     # Llamamos ala superclase
    #     object = super(detalle_establecimiento, self).get_object()
    #     # Grabamos el ultimo acceso ala base de datos
    #     #object.last_accessed = datetime.datetime.now()
    #     object.save()
    #     # Retornamos el objeto
    #     return object