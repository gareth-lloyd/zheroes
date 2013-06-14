from django.conf.urls import patterns, url

from smslink.views import sms_received

urlpatterns = patterns('',
    url(r'^sms/$', sms_received, name="sms-received"),
)
