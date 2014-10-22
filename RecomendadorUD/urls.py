import autocomplete_light
autocomplete_light.autodiscover()

from django.conf.urls import patterns, include, url
from django.contrib import admin
#from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

# from djrill import DjrillAdminSite
# admin.site = DjrillAdminSite()
admin.autodiscover()
#dajaxice_autodiscover()

#from yawdadmin import admin_site
urlpatterns = patterns('',    	
	#url(r'^admin_tools/', include('admin_tools.urls')),
	
    url(r'^admin/', include(admin.site.urls)),        
    url(r'^', include('apps.account_system.urls')),    
    url(r'^', include('apps.establishment_system.urls')),    
    url(r'^', include('apps.recommender_system.urls')),     
    url(r'^', include('apps.main.urls')),     
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if 'grappelli' in settings.INSTALLED_APPS:
		urlpatterns+=patterns('',url(r'^grappelli/', include('grappelli.urls')))


from django.utils.functional import curry
from django.views.defaults import page_not_found, server_error, permission_denied
#handler404 = "apps.main.views.error404"
handler500 = curry(server_error, template_name='main/500.html')
handler404 = curry(page_not_found, template_name='main/404.html')
#handler403 = curry(permission_denied, template_name='main/403.html')