from django.conf.urls.defaults import * #@UnusedWildImport
from app import views as scrapr_views


urlpatterns = patterns('',
  # These are 'named' urls -- tags, search and main, respectively. We can use these to avoid
  # having to manually specify urls all over (but for the sake of this project, we don't).
  url(r'^tags/$', scrapr_views.tags, {}, 'tags'),
  url(r'^tags/search/$', scrapr_views.search, {}, 'search'),
  url(r'^$', scrapr_views.main, {}, 'main'),
)
