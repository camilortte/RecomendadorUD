from django.conf.urls import patterns, include, url
from .views import About, Home

urlpatterns = patterns('',
    
    url(r'^about/$', About.as_view(),name="about_url"),
    url(r'^$', Home.as_view(), name='home_url'),         
    url(r'^home/', Home.as_view(), name='home_url_'), 
)
