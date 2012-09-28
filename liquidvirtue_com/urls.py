from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'liquidvirtue.views.index', name='index'),
    #(r'^id/(\d+)/$', 'liquidvirtue.views.index_with_id', name='index_with_id'),
	url(r'^newest/(?P<page_number>\d+)/$', 'liquidvirtue.views.trackbox_newest', name='trackbox_newest'),
	url(r'^popular/(?P<page_number>\d+)/$', 'liquidvirtue.views.trackbox_popular', name='trackbox_popular'),
	url(r'^my_library/(?P<page_number>\d+)/$', 'liquidvirtue.views.trackbox_my_library', name='trackbox_my_library'),
	url(r'^pagebox/(?P<page_type>\s+)/(?P<page_number>\d+)/$', 'liquidvirtue.views.pagebox', name='pagebox'),
	url(r'^trackinfo/$', 'liquidvirtue.views.trackinfo', name='trackinfo'),
    #
    (r'^facebook/', include('django_facebook.urls')),
    
    #what to do with these?
    (r'^accounts/', include('django_facebook.auth_urls')),
    
    # Example:
    # (r'^django_facebook_test/', include('django_facebook_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.MODE == 'userena':
    urlpatterns += patterns('',
        (r'^accounts/', include('userena.urls')),
    )
elif settings.MODE == 'django_registration':
    urlpatterns += patterns('',
        (r'^accounts/', include('registration.backends.default.urls')),
    )


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
