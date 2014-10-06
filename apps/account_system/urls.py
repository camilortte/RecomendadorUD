# -*- encoding: utf-8 -*-

"""
    
    urls.py: Urls del sistema de usuarios

    @author     Camilo Ramírez
    @contact    camilolinchis@gmail.com 
                camilortte@hotmail.coms
                @camilortte on Twitter
    @copyright  Copyright 2014-2015, RecomendadorUD
    @license    GPL
    @date       2014-10-10
    @satus      Pre-Alpha
    @version=   0..215


"""

from django.conf.urls import patterns, include, url
from .views import (
    LoginViewWithCustomForm,RegistroConvencioanl, 
    RegistroSocial, ProfileUpdate,ProfileUser,
    PorfilesUsers, NotificacionesView,
    MarcarTodasNotificacionesLeidas, MarcarNotificacionLeida)

urlpatterns = patterns('',    

    url(r'^accounts/login', LoginViewWithCustomForm.as_view(),name='login_url'),    
    url(r'^accounts/signup/', RegistroConvencioanl.as_view(),name='signup_url'),
    url(r'^accounts/profile/$', ProfileUser.as_view(),name='profile_url'),
    url(r'^accounts/profile/(?P<pk>\d+)/$', PorfilesUsers.as_view(), name='profiles_url'), 
    url(r'^accounts/social/signup/', RegistroSocial.as_view(),name='signup_url'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout',{'next_page': 'home_url'},name='logout_url'),    
    url(r'^accounts/notifications/', NotificacionesView.as_view() ,name='notificaciones_url'),
    url(r'^accounts/update/',ProfileUpdate.as_view(), name='update_profile_url'),                 
    url(r'^accounts/', include('allauth.urls')),        
    url('', include('django.contrib.auth.urls', namespace='auth')),  
    url(r'^avatar/', include('avatar.urls')),       
    url(r'^mark_as_read_all/$', MarcarTodasNotificacionesLeidas.as_view(), name='mark_as_read_all_url'),
    url(r'^mark_as_read_only/$', MarcarNotificacionLeida.as_view(), name='mark_as_read_only'),


    #url(r'^prueba/','apps.account_system.views.send_notification', name='prueba_url'), 
    #url(r'^accounts/passpass/$', ChangePass.as_view() ,name='account_my_set_password'),
    #url(r'^accounts/updatepass/','apps.account_system.views.change_password', name='change_password_url'),    
)

if True:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
