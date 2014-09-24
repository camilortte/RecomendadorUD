# -*- encoding: utf-8 -*-

"""
    
    context_proccessosrs.py: Se encarga de cargar contexto de manera global.

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

def notificaciones(request):   
    """
        Carga las notificaciones de manera global     
    """
    try:
        notifications = request.user.notifications.unread().order_by('-timestamp')[:5]                  
        return  {'notifications':notifications}
    except( Exception ):
        print "A error occurred : Anonimous user"

    return {}
    
    
