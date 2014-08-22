from django.conf.urls import patterns, include, url
from django.contrib import admin
from djrill import DjrillAdminSite
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

admin.site = DjrillAdminSite()
admin.autodiscover()
dajaxice_autodiscover()


urlpatterns = patterns('',    
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^', include('apps.account_system.urls')),    
    url(r'^', include('apps.establishment_system.urls')),    
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()