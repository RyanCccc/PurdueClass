from django.conf.urls import patterns, include, url

urlpatterns = patterns('course.views',
    url(r'subject/(?P<subject>[a-zA-Z]+)/$', 'subject'),
    url(r'subject/(?P<subject>[a-zA-Z]+)/(?P<CNBR>[0-9a-zA-Z]+)/$', 'courses'),
)
