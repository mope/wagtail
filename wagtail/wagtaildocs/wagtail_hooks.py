from django.conf.urls import include, url
from django.contrib.auth.models import Permission
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailadmin.search import SearchArea
from wagtail.wagtailadmin.site_summary import SummaryItem
from wagtail.wagtailcore import hooks
from wagtail.wagtaildocs import admin_urls
from wagtail.wagtaildocs.models import get_document_model
from wagtail.wagtaildocs.permissions import permission_policy
from wagtail.wagtaildocs.rich_text import DocumentLinkHandler


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^documents/', include(admin_urls, app_name='wagtaildocs', namespace='wagtaildocs')),
    ]


class DocumentsMenuItem(MenuItem):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


@hooks.register('register_admin_menu_item')
def register_documents_menu_item():
    return DocumentsMenuItem(
        _('Documents'),
        urlresolvers.reverse('wagtaildocs:index'),
        name='documents',
        classnames='icon icon-doc-full-inverse',
        order=400
    )


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        static('wagtaildocs/js/hallo-plugins/hallo-wagtaildoclink.js'),
        static('wagtaildocs/js/document-chooser.js'),
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}"></script>',
        ((filename, ) for filename in js_files)
    )
    return js_includes + format_html(
        """
        <script>
            window.chooserUrls.documentChooser = '{0}';
            registerHalloPlugin('hallowagtaildoclink');
        </script>
        """,
        urlresolvers.reverse('wagtaildocs:chooser')
    )


@hooks.register('register_permissions')
def register_permissions():
    return Permission.objects.filter(content_type__app_label='wagtaildocs',
                                     codename__in=['add_document', 'change_document'])


@hooks.register('register_link_chooser')
def register_document_link_chooser():
    return DocumentLinkHandler()


class DocumentsSummaryItem(SummaryItem):
    order = 300
    template = 'wagtaildocs/homepage/site_summary_documents.html'

    def get_context(self):
        return {
            'total_docs': get_document_model().objects.count(),
        }


@hooks.register('construct_homepage_summary_items')
def add_documents_summary_item(request, items):
    items.append(DocumentsSummaryItem(request))


class DocsSearchArea(SearchArea):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


@hooks.register('register_admin_search_area')
def register_documents_search_area():
    return DocsSearchArea(
        _('Documents'), urlresolvers.reverse('wagtaildocs:index'),
        name='documents',
        classnames='icon icon-doc-full-inverse',
        order=400)
