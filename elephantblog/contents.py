from datetime import datetime

from django.db import models
from django.template.loader import render_to_string
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

from elephantblog.models import Category, Entry


class EntryTeaserContent(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, help_text=_('Choose a category. if you omit this field, all categories are displayed.'))
    num_entries = models.PositiveSmallIntegerField(_('Number of entries'), default=2)
    
    class Meta:
        abstract = True
        verbose_name = _('Entry teaser content')
        verbose_name_plural = _('Entry teaser contents')
    
    def render(self, request, **kwargs):
        if self.category:
            entries = Entry.objects.active().filter(categories=self.category)[:self.num_entries]
        else:
            entries = Entry.objects.active()[:self.num_entries]
        
        return render_to_string('content/blog/entry_teaser.html', 
                                {'content' : self, 'entries' : entries})


class BlogDateFilterContent(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('Blog date filter content')
        verbose_name_plural = _('Blog date filter contents')
    
    def render(self, request, **kwargs):
        dates_dict = SortedDict()

        if 'displayed_categories' in request._feincms_extra_context:
            queryset = Entry.objects.active().filter(categories__in=request._feincms_extra_context['displayed_categories'])
        else:
            queryset = Entry.objects.active()

        entry_dates = queryset.order_by('-published_on')\
                                   .values_list('published_on', flat=True)
        
        for date in entry_dates:
            if not date.year in dates_dict:
                dates_dict[date.year] = SortedDict({'date' : datetime(date.year, 1, 1),
                                                    'months' : SortedDict()})
            if not date.month in dates_dict[date.year]['months']:
                dates_dict[date.year]['months'][date.month] = \
                    SortedDict({'date' : datetime(date.year, date.month, 1),
                                'days' : SortedDict()})
            if not date.day in dates_dict[date.year]['months'][date.month]['days']:
                dates_dict[date.year]['months'][date.month]['days'][date.day] = \
                    SortedDict({'date' : datetime(date.year, date.month, date.day)})
        
        return render_to_string('content/blog/date_filter.html', 
                                {'content' : self, 'dates_dict' : dates_dict})


class BlogCategoriesFilterContent(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('Blog categories filter')
        verbose_name_plural = _('Blog categories filter')

    def render(self, request, **kwargs):
        if 'displayed_categories' in request._feincms_extra_context:
            categories = Category.objects.filter(id__in=request._feincms_extra_context['displayed_categories'])
        else:
            categories = Category.objects.all()

        return render_to_string('content/blog/category_filter.html',
                               {'content' : self, 'categories' : categories})
