from __future__ import absolute_import, print_function, unicode_literals

import bisect
import operator

from django.forms.utils import flatatt
from django.utils.functional import cached_property
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page


class LinkChooserRegistry(object):

    def add(self, item, priority=900):
        bisect.insort(self.items, (priority, item))

    def remove(self, item):
        self.items = [pair for pair in self.items if pair[1] != item]

    @cached_property
    def items(self):
        registered_hooks = hooks.get_hooks('register_rich_text_link_chooser')
        return sorted({hook() for hook in registered_hooks},
                      key=operator.attrgetter('priority'))

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)


registry = LinkChooserRegistry()


class InternalLinkChooser(object):
    """
    PageLinkHandler will be invoked whenever we encounter an <a> element in
    HTML content with an attribute of data-linktype="page". The resulting
    element in the database representation will be: <a linktype="page"
    id="42">hello world</a>
    """

    id = 'page'
    title = _('Internal link')
    url_name = 'wagtailadmin_choose_page'
    priority = 100

    @staticmethod
    def get_db_attributes(tag):
        """
        Given an <a> tag that we've identified as a page link embed (because it has a
        data-linktype="page" attribute), return a dict of the attributes we should
        have on the resulting <a linktype="page"> element.
        """
        return {'id': tag['data-id']}

    @staticmethod
    def expand_db_attributes(attrs, for_editor):
        try:
            page = Page.objects.get(id=attrs['id'])

            if for_editor:
                editor_attrs = 'data-linktype="page" data-id="%d" ' % page.id
            else:
                editor_attrs = ''

            return '<a %shref="%s">' % (editor_attrs, escape(page.url))
        except Page.DoesNotExist:
            return "<a>"


class SimpleLinkChooser(object):
    @classmethod
    def get_db_attributes(cls, tag):
        return {'href': tag['href']}

    @classmethod
    def expand_db_attributes(cls, attrs, for_editor):
        attrs = {'href': attrs['href']}
        if for_editor:
            attrs['data-linktype'] = cls.id
        return '<a{}>'.format(flatatt(attrs))


class ExternalLinkChooser(SimpleLinkChooser):
    id = 'external'
    title = _('External link')
    url_name = 'wagtailadmin_choose_page_external_link'
    priority = 200


class EmailLinkChooser(SimpleLinkChooser):
    id = 'email'
    title = _('Email link')
    url_name = 'wagtailadmin_choose_page_email_link'
    priority = 300