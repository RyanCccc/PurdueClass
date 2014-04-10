from django.conf.urls import patterns, include, url

urlpatterns = patterns('pu_class.views',
    url(r'all/(?P<term>[a-zA-Z0-9]+)/$', 'get_all_by_term'),
    url(r'catalogs/(?P<term>[a-zA-Z0-9]+)/$', 'get_all_cat_by_term'),
    url(r'seats/$', 'get_seats_by_term'),
)
