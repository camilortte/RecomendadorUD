from django.conf.urls import patterns, include, url
from .views import test

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.Main.views.test'),
    # url(r'^blog/', include('blog.urls')),
)
