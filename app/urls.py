from django.conf.urls.defaults import * #@UnusedWildImport
from scrapr.app import views as scrapr_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  # These are 'named' urls -- search and main, respectively.
  url(r'^search/$', scrapr_views.search, {}, 'search'),
  url(r'^$', scrapr_views.main, {}, 'main'),
    # Example:

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
