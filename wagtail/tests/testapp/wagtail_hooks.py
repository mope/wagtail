from __future__ import absolute_import, unicode_literals

from django.forms.utils import flatatt
from django.http import HttpResponse

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailadmin.search import SearchArea
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import (
    allow_without_attributes, attribute_rule, check_url)


# Register one hook using decorators...
@hooks.register('insert_editor_css')
def editor_css():
    return """<link rel="stylesheet" href="/path/to/my/custom.css">"""


def editor_js():
    return """<script src="/path/to/my/custom.js"></script>"""
hooks.register('insert_editor_js', editor_js)
# And the other using old-style function calls


def whitelister_element_rules():
    return {
        'blockquote': allow_without_attributes,
        'a': attribute_rule({'href': check_url, 'target': True}),
    }
hooks.register('construct_whitelister_element_rules', whitelister_element_rules)


def block_googlebot(page, request, serve_args, serve_kwargs):
    if request.META.get('HTTP_USER_AGENT') == 'GoogleBot':
        return HttpResponse("<h1>bad googlebot no cookie</h1>")
hooks.register('before_serve_page', block_googlebot)


class KittensMenuItem(MenuItem):
    def is_shown(self, request):
        return not request.GET.get('hide-kittens', False)


@hooks.register('register_admin_menu_item')
def register_kittens_menu_item():
    return KittensMenuItem(
        'Kittens!',
        'http://www.tomroyal.com/teaandkittens/',
        classnames='icon icon-kitten',
        attrs={'data-fluffy': 'yes'},
        order=10000
    )


# Admin Other Searches hook
class MyCustomSearchArea(SearchArea):
    def is_shown(self, request):
        return not request.GET.get('hide-option', False)

    def is_active(self, request, current=None):
        return request.GET.get('active-option', False)


@hooks.register('register_admin_search_area')
def register_custom_search_area():
    return MyCustomSearchArea(
        'My Search',
        '/customsearch/',
        classnames='icon icon-custom',
        attrs={'is-custom': 'true'},
        order=10000)


class FooLinkHandler(object):
    @staticmethod
    def get_db_attributes(tag):
        return {'foo': tag.attrs['data-foo']}

    @staticmethod
    def expand_db_attributes(attrs, for_editor):
        new_attrs = {'href': 'http://example.com/{}/'.format(attrs['foo'])}
        if for_editor:
            new_attrs.update({
                'data-foo': attrs['foo'],
                'data-linktype': 'foo',
            })
        return '<a{}>'.format(flatatt(new_attrs))


# RemovedInWagtail16Warning
@hooks.register('register_rich_text_link_handler')
def register_foo_link_handler():
    return ('foo', FooLinkHandler())
