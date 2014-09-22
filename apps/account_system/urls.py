# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import (
    LoginViewWithCustomForm,SignupViewMio, 
    SignupSocialView, ProfileUpdate,ProfileUser,
    PorfilesUsers, NotificacionesView)
from django.conf import settings




urlpatterns = patterns('',    
    url(r'^$', 'apps.account_system.views.home', name='home_url'),         
    url(r'^home/', 'apps.account_system.views.home', name='home_url_'), 

    url(r'^accounts/login', LoginViewWithCustomForm.as_view(),name='login_url'),    
    url(r'^accounts/signup/', SignupViewMio.as_view(),name='signup_url'),
    url(r'^accounts/profile/$', ProfileUser.as_view(),name='profile_url'),
    url(r'^accounts/profile/(?P<pk>\d+)/$', PorfilesUsers.as_view(), name='profiles_url'), 
    url(r'^accounts/social/signup/', SignupSocialView.as_view(),name='signup_url'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout',
                          {'next_page': 'home_url'},name='logout_url'),
    url(r'^accounts/notifications/', NotificacionesView.as_view() ,name='notificaciones_url'),
    url(r'^accounts/update/',ProfileUpdate.as_view(), name='update_profile_url'),             
    url(r'^accounts/updatepass/','apps.account_system.views.change_password', name='change_password_url'),    
    url(r'^accounts/', include('allauth.urls')),        
    url('', include('django.contrib.auth.urls', namespace='auth')),  
    url(r'^avatar/', include('avatar.urls')),  
    url(r'^prueba/','apps.account_system.views.send_notification', name='prueba_url'),  
    url(r'^mark_as_read_all/$', 'apps.account_system.views.mark_as_read_all', name='mark_as_read_all_url'),
    url(r'^mark_as_read_only/$', 'apps.account_system.views.marcar_notificacion_como_leida', name='mark_as_read_only'),
)

if True:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
