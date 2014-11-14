from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^home/$', 'explore.views.home', name='home'),
    url(r'^$', 'explore.views.home', name='home'),

    # dispatch
    url(r'^receive_code/', 'explore.views.callback' ), 

    # user info 
    url(r'^user/$', 'explore.views.user_request'),
    url(r'^names/$', 'explore.views.names_request'),

    url(r'^genomes/$', 'explore.views.redirect_genome_request'),

    url(r'^neanderthal/$', 'explore.views.neanderthal_request'),

    # error routing
    url(r'^/forbidden/', TemplateView.as_view(template_name='forbidden.html')),
    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += staticfiles_urlpatterns()

