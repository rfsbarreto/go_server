from django.conf.urls import include, url

from django.contrib import admin
from welcome.views import health
admin.autodiscover()

import web.views
import gobus.views
import gotrack.views


# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', web.views.index, name='index'),
    url(r'^health$', health),
    url(r'^go_bus/record/', gobus.views.go_bus_record, name='go_bus_record'),
    url(r'^go_track/record/', gotrack.views.go_track_record, name='go_track_record'),
    url(r'^welcome/', include('welcome.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
