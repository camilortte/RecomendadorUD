from django.utils import simplejson
from dajaxice.decorators import dajaxice_register


@dajaxice_register
def dajaxice_example(request):	
    return simplejson.dumps({'message':'Hello from Python!'})


"""Marca las notificaciones leidas mediante AJAX
responde con el numero actual de notificaciones no vistas
y con el id eliminado"""
@dajaxice_register
def mark_as_read_only(request, id):
	usuario=request.user
	#obtengo el id
	notificacion=usuario.notifications.filter(id=id)
	notificacion.mark_all_as_read()
	count = usuario.notifications.unread().count()
	return simplejson.dumps({'id_leido':id,'count':count})