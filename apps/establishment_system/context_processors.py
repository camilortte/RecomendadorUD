def notificaciones(request):        
    try:
        notifications = request.user.notifications.unread().order_by('-timestamp')[:10]                  
        return 	{'notifications':notifications}
    except( Exception ):
        print "A error occurred : Anonimous user"

    return {}
    
    