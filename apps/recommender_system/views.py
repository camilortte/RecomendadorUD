# -*- encoding: utf-8 -*-
"""
    
    views: vistas sistema recomendador

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
from django.views.generic import TemplateView
from apps.recommender_system.models import EstablecimientosRecommender
from apps.establishment_system.models import Establecimiento
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.externals.djangoratings.models import Vote


class RecomendacionView(TemplateView):
    template_name = 'recommender/recomendacion.html'    

    def get_context_data(self, **kwargs):        
        context = super(RecomendacionView, self).get_context_data(**kwargs)
        #context['now'] = timezone.now()
        context['recomendaciones']=self.obtener_recomendacion(self.request.user)
        return context

    def obtener_recomendacion(self,user):
        print "Prediciendo recomendacion"
        recomendador_instance=EstablecimientosRecommender()
        recomendaciones=recomendador_instance.storage.get_recommendations_for_user(user)
        print recomendaciones
        if recomendaciones:
            print "Recomendando"
            result=[]
            for recomendacion in recomendaciones:
                result.append(recomendacion.object)
            recomendaciones=result

            recomendaciones_leng=len(recomendaciones)
            if recomendaciones_leng <10:
                query=Establecimiento.objects.all().order_by('-rating_score')
                for establecimiento in query:
                    if establecimiento not in recomendaciones:
                        if not Vote.objects.filter(object_id=establecimiento.id,user=user.id):
                            recomendaciones.append(establecimiento)
                            if len(recomendaciones)>=10:
                                break
               
        else:
            query=Establecimiento.objects.all().order_by('-rating_score')
            for establecimiento in query:
                if establecimiento not in recomendaciones:
                    if not Vote.objects.filter(object_id=establecimiento.id,user=user.id):
                        recomendaciones.append(establecimiento)
                        if len(recomendaciones)>=10:
                            print "Se completo la lista de 10 recomendaciones"
                            break
            print "No se encontraron recomendaciones"
        return recomendaciones

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecomendacionView, self).dispatch(*args, **kwargs)




