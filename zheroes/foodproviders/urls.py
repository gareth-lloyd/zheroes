from django.conf.urls import patterns, url

from foodproviders.views import MapView, filter_fps

urlpatterns = patterns('',
    url(r'^$', MapView.as_view(), name="map"),
    url(r'^filter/$', filter_fps, name="filter"),
)
