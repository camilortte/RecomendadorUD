from django.views.generic.base import View
from django.views.generic import TemplateView
from django.shortcuts import render
from apps.establishment_system.models import Establecimiento
# Create your views here.
 
class Test(View):
 
    def get(self, request):
        # TODO: GET ACTIONS
        return render(request,"Main/index.html")
 
    def post(self, request):
        # TODO: POST ACTIONS
        return render(request,"Main/index.html")
 
    def put(self, request):
        # TODO: PUT ACTIONS
        return render(request,"Main/index.html")
 
    def delete(self, request):
        # TODO: DELETE ACTIONS
        return render(request,"Main/index.html")


class About(TemplateView):
    template_name="main/about.html"


class Home(TemplateView):
    template_name="main/home.html"

    def dispatch(self, *args, **kwargs):
        return super(Home, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
            Se agrega el contexto 
        """
        context = super(Home, self).get_context_data(**kwargs)
        context['cantidad']=Establecimiento.objects.count()
        return context

def error404(request):
    return render(request,'main/404.html', status=404)