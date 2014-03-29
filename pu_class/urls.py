from django.conf.urls import patterns, include, url

urlpatterns = patterns('pu_class.views',
    url(r'all/(?P<term>[a-zA-Z0-9]+)/$', 'get_all_by_term'),
)