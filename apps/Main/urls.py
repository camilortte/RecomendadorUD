from django.conf.urls import patterns, include, url
from .views import Test

urlpatterns = patterns('',
    
    url(r'^prueba1$', Test.as_view()),
    
)
