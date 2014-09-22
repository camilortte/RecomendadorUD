from django.views.generic.base import View
from django.views.generic import TemplateView
from django.shortcuts import render

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