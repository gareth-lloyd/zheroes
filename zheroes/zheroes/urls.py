from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sms/', include('smslink.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
