from django.db import models
from django.template.loader import render_to_string
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
