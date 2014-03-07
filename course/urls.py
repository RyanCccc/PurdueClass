from django.conf.urls import patterns, include, url

urlpatterns = patterns('course.views',
    url(r'subject/(?P<subject>[a-z]+)/$', 'subject'),
    url(r'subject/(?P<subject>[a-z]+)/(?P<CNBR>[0-9a-z]+)/$', 'courses'),
)
