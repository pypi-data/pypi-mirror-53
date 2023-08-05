from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils import get_language_list

from django.utils.translation import get_language, ugettext_lazy as _

from . import models


@toolbar_pool.register
class ImageExtensionToolbar(ExtensionToolbar):
    model = models.ImageExtension

    def populate(self):
        # setup the extension toolbar with permissions and sanity checks
        current_page_menu = self._setup_extension_toolbar()
        # if it's all ok
        if current_page_menu:
            # retrieves the instance of the current extension (if any) and the toolbar item url
            page_extension, url = self.get_page_extension_admin()
            if url:
                # adds a toolbar item
                current_page_menu.add_modal_item(_('Page Image'), url=url,
                    disabled=not self.toolbar.edit_mode_active)


@toolbar_pool.register
class TeaserExtensionToolbar(ExtensionToolbar):
    model = models.TeaserExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu:
            urls = self.get_title_extension_admin()
            page = self._get_page()
            titleset = page.title_set.filter(language__in=get_language_list(page.node.site_id))

            nodes = [
                (title_extension, url, title.title)
                for ((title_extension, url), title)
                in zip(urls, titleset)
            ]

            for title_extension, url, title in nodes:
                current_page_menu.add_modal_item(
                    _('Teaser for {}'.format(title)), url=url,
                    disabled=not self.toolbar.edit_mode_active
                )
