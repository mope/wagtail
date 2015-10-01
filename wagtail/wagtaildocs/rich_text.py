from django.utils.html import escape

from wagtail.wagtailadmin.link_choosers import LinkChooser
from wagtail.wagtaildocs.models import Document

from django.utils.translation import ugettext_lazy as _


class DocumentLinkHandler(LinkChooser):

    id = 'document'
    title = _('Document')
    url_name = 'wagtaildocs:chooser'
    priority = 400

    @staticmethod
    def get_db_attributes(tag):
        return {'id': tag['data-id']}

    @staticmethod
    def expand_db_attributes(attrs, for_editor):
        try:
            doc = Document.objects.get(id=attrs['id'])

            if for_editor:
                editor_attrs = 'data-linktype="document" data-id="%d" ' % doc.id
            else:
                editor_attrs = ''

            return '<a %shref="%s">' % (editor_attrs, escape(doc.url))
        except Document.DoesNotExist:
            return "<a>"
