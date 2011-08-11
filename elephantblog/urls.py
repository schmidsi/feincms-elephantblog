from django.conf import settings
from django.conf.urls.defaults import *

from feincms.translations import short_language_code

from models import Entry
from feeds import EntryFeed

"""
The entry dict here is only interpreted during server initialization.
"""
entry_dict = {
    'paginate_by' : 10,
    }

urlpatterns = patterns('',
    url(r'^feed/$', EntryFeed()),
    url(r'^headlines/$', 'elephantblog.views.entry_list', 
        dict(entry_dict, template_name='blog/entry_headlines.html'), name='elephantblog_headlines'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$', 
        'elephantblog.views.entry', name='elephantblog_entry_detail'),
    
    url(r'^$', 
        'elephantblog.views.entry_list', entry_dict, name='elephantblog_list'),
    url(r'^category/(?P<category>[\w-]+)/$', 
        'elephantblog.views.entry_list', name='elephantblog_category_list'),
    url(r'^(?P<year>\d{4})/$', 
        'elephantblog.views.entry_list', entry_dict, name='elephantblog_year_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 
        'elephantblog.views.entry_list', entry_dict, name='elephantblog_month_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 
        'elephantblog.views.entry_list', entry_dict, name='elephantblog_day_list'),
    #url(r'^(category/(?P<category>[\w-]+)/)?((?P<year>\d{4})/)?((?P<month>\d{2})/)?((?P<day>\d{2})/)?$', 'elephantblog.views.entry_list', entry_dict, name='elephantblog_list'),
)

#if 'tagging' in settings.INSTALLED_APPS:
#    urlpatterns += patterns('',url(r'^tag/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list',
#        { 'template_name':'entry_list_tagged.html', 'paginate_by':entry_dict['paginate_by']}, name='elephantblog_tag'),
#)

