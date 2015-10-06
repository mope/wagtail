from django.core import urlresolvers
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks

from .menu import MenuItem, SubmenuMenuItem, settings_menu
from .link_choosers import (
    InternalLinkChooser, ExternalLinkChooser, EmailLinkChooser)


class ExplorerMenuItem(MenuItem):
    class Media:
        js = ['wagtailadmin/js/explorer-menu.js']


@hooks.register('register_admin_menu_item')
def register_explorer_menu_item():
    return ExplorerMenuItem(
        _('Explorer'), urlresolvers.reverse('wagtailadmin_explore_root'),
        name='explorer',
        classnames='icon icon-folder-open-inverse dl-trigger',
        attrs={'data-explorer-menu-url': urlresolvers.reverse('wagtailadmin_explorer_nav')},
        order=100)


@hooks.register('register_admin_menu_item')
def register_settings_menu():
    return SubmenuMenuItem(
        _('Settings'), settings_menu, classnames='icon icon-cogs', order=10000)


@hooks.register('register_permissions')
def register_permissions():
    return Permission.objects.filter(content_type__app_label='wagtailadmin', codename='access_admin')


@hooks.register('register_rich_text_link_chooser')
def register_internal_link_chooser():
    return InternalLinkChooser()


@hooks.register('register_rich_text_link_chooser')
def register_external_link_chooser():
    return ExternalLinkChooser()


@hooks.register('register_rich_text_link_chooser')
def register_email_link_chooser():
    return EmailLinkChooser()
