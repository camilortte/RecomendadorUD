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
        recomendador_instance=EstablecimientosRecommender()
        recomendaciones=recomendador_instance.storage.get_recommendations_for_user(user)
        if recomendaciones:
            result=[]
            print "tenemos resultados: ",recomendaciones         
            for recomendacion in recomendaciones:
                print "Esto es recomendaciones: ",recomendaciones
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
            print "No tenemos resultadso"
            recomendaciones=Establecimiento.objects.all().order_by('rating_score')[:10]
        return recomendaciones

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecomendacionView, self).dispatch(*args, **kwargs)




