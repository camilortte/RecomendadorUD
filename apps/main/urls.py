from django.conf.urls import patterns, include, url
from .views import About

urlpatterns = patterns('',
    
    url(r'^about/$', About.as_view(),name="about_url"),
    
)
