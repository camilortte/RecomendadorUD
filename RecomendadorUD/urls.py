from django.conf.urls import patterns, include, url
from django.contrib import admin
from djrill import DjrillAdminSite
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.site = DjrillAdminSite()
admin.autodiscover()
dajaxice_autodiscover()


urlpatterns = patterns('',    
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^', include('apps.account_system.urls')),    
    url(r'^', include('apps.establishment_system.urls')),    
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()