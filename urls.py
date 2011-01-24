from django.conf.urls.defaults import * #@UnusedWildImport
from django.views import generic as generic_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', generic_views.RedirectView.as_view(url = '/app/')),
  
  # Namespaced includes allow you perform nice reverse url lookups. See
  # http://docs.djangoproject.com/en/1.2/topics/http/urls/#including-other-urlconfs
	(r'^app/', include('scrapr.app.urls', namespace = 'app', app_name = 'app')),
	
	# Uncomment the admin/doc line below to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	# Uncomment the next line to enable the admin:
	# (r'^admin/', include(admin.site.urls)),
)
