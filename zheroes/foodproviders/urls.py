from django.conf.urls import patterns, url

from foodproviders.views import MapView

urlpatterns = patterns('',
    url(r'^$', MapView.as_view(), name="map"),
)
